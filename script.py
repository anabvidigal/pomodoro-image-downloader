import requests, os, bs4
from selenium import webdriver, common
from selenium.webdriver.common.by import By

list = [
    "Tomato",
    "Cherry Tomato",
    "Tomato Soup",
    "Bloody Mary",
    "Bruschetta",
    "Pizza",
    "Caprese",
    "Tomato sauce"
]

def download_images(browser, item, amount):
    # Download all images
    try:
        imageElems = browser.find_elements(By.CSS_SELECTOR, 'a.overlay')
        for element in imageElems[:amount]:
            downloadUrl = element.get_attribute("href") + "sizes/o/"
            res = requests.get(downloadUrl)
            res.raise_for_status()

            soup = bs4.BeautifulSoup(res.text, "lxml")
            imageElem = soup.select("img")

            if not imageElem:
                print("Could not find image.")
            else:
                imageUrl = imageElem[2].get("src")

                # Skip gifs
                if imageUrl.endswith(".gif"):
                    print(f"Skipped .gif file: {imageUrl}")
                    continue

                # Save image to ./images
                res = requests.get(imageUrl)
                res.raise_for_status()

                imageFile = open(os.path.join(f"images/{item}", os.path.basename(imageUrl)), "wb")
                for chunk in res.iter_content(100000):
                    imageFile.write(chunk)
                imageFile.close()

    except common.exceptions.NoSuchElementException as err:
        print("Unable to locate element: %s" % err)

def main():

    # Open Browser to photo-sharing site
    url = "https://www.flickr.com/search/?text=" # starting url

    browser = webdriver.Firefox()
    browser.implicitly_wait(10) # seconds

    for item in list:
        # Search for category of photos
        browser.get(url + item)

        # store images in ./images
        os.makedirs(f"images/{item}", exist_ok=True)

        download_images(browser, item, amount=8)

    browser.quit()

if __name__ == '__main__':
    main()
