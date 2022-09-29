# Details: Python scripts to download given no. of images on to the folder from google search engine
# install all module before running

from bs4 import BeautifulSoup
import os
import sys
import requests
import shutil


def image_downloader(keyword='nature', num=5):
    # Creating a new folder with name of given keyword, if not present
    # Folder would be created in the same path as that of this module
    # All images would be downloaded to the folder automatically
    if not os.path.exists(keyword):
        os.makedirs(keyword)

    url = "https://www.google.co.in/search?q="+keyword+"&source=lnms&tbm=isch"
    header = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    page = requests.get(url, headers=header)

    # Parsing the query url using beautiful soup library
    soup = BeautifulSoup(page.text,'html.parser')
    ActualImages = []
    i = 1

    for a in soup.find_all("div", {"class": "NZWO1b"}):
        if a and a.img:
            ActualImages.append(a.img["src"])
            i += 1
            if i > num:
                break
    i = 1
    for img_url in ActualImages:
        try:
            res = requests.get(img_url, stream=True)
            # path and file name of image to be saved in the path
            file_name = os.path.join(keyword, keyword.split()[0] + "-img-" + str(i) + ".jpg")
            if res.status_code == 200:
                with open(file_name, 'wb') as f:
                    shutil.copyfileobj(res.raw, f)
                print(f'Image {file_name } successfully downloaded: ')
                i += 1
            else:
                print('Image could not be retrieved')
        except Exception as e:
            print(f"Error: could not load the url :{img_url}")
            print(e)


if __name__ == '__main__':
    try:
        keyword = input("Enter the search keyword for image: ")
        num = int(input("Enter the number of image to be downloaded: "))
        # input taken from system directly,  use below
        # keyword = str(sys.argv[1])
        # num = int(sys.argv[2])
        image_downloader(keyword, num)
    except KeyboardInterrupt:
        pass
    sys.exit()
