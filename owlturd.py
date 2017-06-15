
#! Python 3
# This is an owlturd-comic downloader from "http://owlturd.com"

import requests
import os
import bs4
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

        if not comicelem:  # if there are no imgs
            print("Could not find comic")
        else:
            for img in range(len(comicelem) - 1):  # for each img on the site
                try:
                    comicurl = comicelem[img].get("src")  # get specific img-url
                    print("-Downloading comic: {}".format(comicurl))
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
        # next page
        count += 1
        url = "http://owlturd.com/page/" + str(count)

if __name__ == "__main__":

    # Start: Validation of use and desired pagenumber to download
    print("This program will download comics from 'owlturd.com'.")
    print("The comics will be downloaded to the directory this .exe is in.")
    print("=" * 45)
    confirm = input("Do you want to download owlturd comics? (y/n) \n >>")
    if confirm.lower() == "y":
        while True:
            try:
                pagecount_test = int(input("How many pages? \n >>"))
                url_test = "http://owlturd.com/page/" + str(pagecount_test)
                res_test = requests.get(url_test)
                res_test.raise_for_status()
                soup_test = bs4.BeautifulSoup(res_test.text, "html.parser")
                comicelem_test = soup_test.select("img.photo-md")
                if not comicelem_test:  # if there are no imgs
                    raise EOFError  # "end of website is reached"
            except (ValueError, EOFError):
                print("There aren't so many pages or input is invalid.")
                continue
            else:
                owlturd_download(pagecount_test)
                print("Done!")
                break
    else:
        sys.exit(0)
