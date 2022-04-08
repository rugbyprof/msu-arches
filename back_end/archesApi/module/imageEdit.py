from PIL import Image
from wand.image import Image
import os
import sys


class ImageEditor:

    def __init__(self):
        pass

    def resizeImage(self, file_path, size=None):
        if not os.path.isfile(file_path):
            print(f"Cannot resize a file that doesn't exist! {file_path}")
            sys.exit()
        if not size:
            print(f"Need a size to ... RESIZE! Really stupid dude.")
            sys.exit()

        dirname = os.path.dirname(file_path)
        justname = os.path.splitext(os.path.basename(file_path))[0]

        img = Image(filename=file_path)
        print(img.width, img.height)
        w, h = size
        img.resize(w, h)
        print(img.width, img.height)
        newname = os.path.join(dirname, justname, f"_resized_{w}x{h}.jpg")
        img.save(filename=newname)

    def cropImage(self, path, ul, lr):
        pass


if __name__ == "__main__":
    pass
