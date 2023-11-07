def main():
    import requests, os, bs4
    from selenium import webdriver, common
    from selenium.webdriver.common.by import By

    # Open Browser to photo-sharing site
    url = "https://www.flickr.com/search/?text=" # starting url
    os.makedirs("images", exist_ok=True) # store images in ./images

    browser = webdriver.Firefox()
    browser.implicitly_wait(10) # seconds

    # Search for category of photos
    browser.get(url + "Tomato")

    # Download all images
    try:
        imageElems = browser.find_elements(By.CSS_SELECTOR, 'a.overlay')
        for element in imageElems[:6]:
            downloadUrl = element.get_attribute("href") + "sizes/o/"
            res = requests.get(downloadUrl)
            res.raise_for_status()

            soup = bs4.BeautifulSoup(res.text, "lxml")
            imageElem = soup.select("img")

            if not imageElem:
                print("Could not find image.")
            else:
                imageUrl = imageElem[2].get("src")

                # Save image to ./images
                res = requests.get(imageUrl)
                res.raise_for_status()

                imageFile = open(os.path.join("images", os.path.basename(imageUrl)), "wb")
                for chunk in res.iter_content(100000):
                    imageFile.write(chunk)
                imageFile.close()

    except common.exceptions.NoSuchElementException as err:
        print("Unable to locate element: %s" % err)

    browser.close()

if __name__ == '__main__':
    main()
