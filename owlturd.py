
#! Python 3
# This is an owlturd-comic downloader from "http://owlturd.com"

import requests
import os
import bs4
import logging
import sys

# the main function of this program
def owlturd_download(pagecount):
    url = "http://owlturd.com/page/1"  # start url
    os.makedirs("owlturd", exist_ok=True)

    for count in range(1, pagecount + 1):  # file 1 to pagecount looping
        print("=" * 42)
        print("Downloading page {}".format(url))
        print("=" * 42)
        res = requests.get(url)
        try:
            res.raise_for_status()  # validation
        except Exception as exc:
            print("An Error {} has occured".format(exc))
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        comicelem = soup.select("img.photo-md")
        logging.warning("len comicElem:" + str(len(comicelem)))

        if not comicelem:  # if there are no imgs
            print("Could not find comic")
        else:
            for img in range(len(comicelem) - 1):  # for each img on the site
                try:
                    comicurl = comicelem[img].get("src")  # get specific img-url
                    print("-Downloading comic: {}".format(comicurl))
                    logging.info(comicurl)
                    res = requests.get(comicurl, stream=True)  # get the img
                    res.raise_for_status()  # validation
                    os.makedirs(os.path.join("owlturd", ("page" + str(count))), exist_ok=True)  # folder for imgs
                except requests.exceptions.MissingSchema:
                    # skip comic
                    continue

                # saving the image
                with open(os.path.join("owlturd", ("page" + str(count)), os.path.basename(comicurl)), "wb") as imagefile:
                    for chunk in res.iter_content(100000):
                        imagefile.write(chunk)
                    imagefile.close()

        url = "http://owlturd.com/" + "page/" + str(count)
        logging.critical(url)

if __name__ == "__main__":

    # This was for testing purposes
    logging.basicConfig(  # filename="dumb.log",
        level=logging.WARNING,
        format="%(asctime)s - %(levelname)s - %(message)s -in function: %(funcName)s")
    logging.disable(logging.CRITICAL)  # now disabled

    # Start: Validation of use and desired pagenumber to download
    print("This program will download comics from 'owlturd.com'.")
    print("The comics will be downloaded to the directory this .exe is in.")
    print("=" * 45)
    confirm = input("Do you want to download owlturd comics? (y/n) \n >>")
    if confirm.lower() == "y":
        while True:
            try:
                pagecount = int(input("How many pages? Max: 77. \n >>"))
            except ValueError:
                print("Enter a number < 77!")
                continue
            if pagecount > 77:
                print("Enter a number < 77!")
                continue
            else:
                owlturd_download(pagecount)
                print("Done!")
                break
    else:
        sys.exit(0)
