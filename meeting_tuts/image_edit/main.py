""" Code from the April 1st research meeting
"""

from PIL import Image
import os
import sys
import glob
from rich import print


def listImages(folder):
    files = glob.glob(os.path.join(folder, "*.jpg"))

    return files


def cropRegion(path, left, top, right, bottom, save_path):
    """
    """
    # check to see if image really exists
    if not os.path.isfile(path):
        print(f"error: {path} is not a valid file!")
        sys.exit()

    # pull the name out of the file path
    parts = path.split("/")  # split path on slashed
    fileName = parts[-1]  # grab last piece which is the name
    name, ext = fileName.split(".")  # split name and extenstion

    im = Image.open(path)  # open the image
    region = im.crop((left, top, right, bottom))  # crop the image

    newName = name + "_cropped" + "." + ext  # create the new name

    region.save(os.path.join(save_path, newName))  # save the new cropped image


if __name__ == '__main__':
    images = listImages('../images/')
    i = 0
    for image in images:
        print(f"{i}: {image}")
        i += 1

    choice = input("Choose image to edit:")

    if len(choice) < 4:
        choice = images[int(choice)]

    cropRegion(choice, 300, 1100, 900, 2300, "../images/cropped")
