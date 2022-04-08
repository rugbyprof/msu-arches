# -*- coding:utf-8 -*-

# Libraries for FastAPI
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Builtin libraries

import os
import sys
import glob

from PIL import Image
from wand.image import Image

# Classes from my module
# from module import CountryReader
# from module import Feature
# from module import FeatureCollection
"""
           _____ _____   _____ _   _ ______ ____
     /\   |  __ \_   _| |_   _| \ | |  ____/ __ \
    /  \  | |__) || |     | | |  \| | |__ | |  | |
   / /\ \ |  ___/ | |     | | | . ` |  __|| |  | |
  / ____ \| |    _| |_   _| |_| |\  | |   | |__| |
 /_/    \_\_|   |_____| |_____|_| \_|_|    \____/

The `description` is the information that gets displayed when the api is accessed from a browser and loads the base route.
Also the instance of `app` below description has info that gets displayed as well when the base route is accessed.
"""

description = """🚀
## Msu Arches
### Finding Arches on Buildings like its a cool thing to do ... even though its not.
"""

# Needed for CORS
origins = ["*"]

# This is the `app` instance which passes in a series of keyword arguments
# configuring this instance of the api. The URL's are obviously fake.
app = FastAPI(
    title="MSU Arches",
    description=description,
    version="0.0.1",
    terms_of_service="http://killzonmbieswith.us/msuarches/terms/",
    contact={
        "name": "Msu Arches",
        "url": "http://killzonmbieswith.us/msuarches/contact/",
        "email": "archie@killzonmbieswith.us",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

# Needed for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""
  _      ____   _____          _         _____ _                _____ _____ ______  _____
 | |    / __ \ / ____|   /\   | |       / ____| |        /\    / ____/ ____|  ____|/ ____|
 | |   | |  | | |       /  \  | |      | |    | |       /  \  | (___| (___ | |__  | (___
 | |   | |  | | |      / /\ \ | |      | |    | |      / /\ \  \___ \\___ \|  __|  \___ \
 | |___| |__| | |____ / ____ \| |____  | |____| |____ / ____ \ ____) |___) | |____ ____) |
 |______\____/ \_____/_/    \_\______|  \_____|______/_/    \_\_____/_____/|______|_____/

This is where you will add code to load all the countries and not just countries. Below is a single
instance of the class `CountryReader` that loads countries. There are 6 other continents to load or
maybe you create your own country file, which would be great. But try to implement a class that 
organizes your ability to access a countries polygon data.
"""


class ImageEditor:
    """ 
    Dependancies: 
        PIL
        Wand (ImageMagick)
    """

    def __init__(self, images_path=None):
        self.imagesPath = images_path

    def resizeImage(self, file_path, size=None):
        if not os.path.isfile(file_path):
            print(f"Cannot resize a file that doesn't exist! {file_path}")
            sys.exit()
        if not size:
            print(f"Need a size to ... RESIZE! Really stupid.")
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


"""
  _      ____   _____          _        __  __ ______ _______ _    _  ____  _____   _____
 | |    / __ \ / ____|   /\   | |      |  \/  |  ____|__   __| |  | |/ __ \|  __ \ / ____|
 | |   | |  | | |       /  \  | |      | \  / | |__     | |  | |__| | |  | | |  | | (___
 | |   | |  | | |      / /\ \ | |      | |\/| |  __|    | |  |  __  | |  | | |  | |\___ \
 | |___| |__| | |____ / ____ \| |____  | |  | | |____   | |  | |  | | |__| | |__| |____) |
 |______\____/ \_____/_/    \_\______| |_|  |_|______|  |_|  |_|  |_|\____/|_____/|_____/

I place local methods either here, or in the module we created. I'm leaving it here to help
with the lecture we had in class, but it can easily be moved then imported. In fact you should
move it if you have other "spatial" methods that it can be packaged with in the module folder. 
"""


def getImageList(path=None):
    """Gets a list of images from the ones needing processed.
    Params:
        None
    Returns:
        List [] : list of all images in specified folder.
    """
    if not path:
        path = "../images"

    path = path.lstrip("/")

    files = []
    for ext in ["jpg", "png", "svg"]:
        f = glob.glob(f"{path}/*.{ext}")
        files.extend(f)

    return sorted(files)


"""
  _____   ____  _    _ _______ ______  _____
 |  __ \ / __ \| |  | |__   __|  ____|/ ____|
 | |__) | |  | | |  | |  | |  | |__  | (___
 |  _  /| |  | | |  | |  | |  |  __|  \___ \
 | | \ \| |__| | |__| |  | |  | |____ ____) |
 |_|  \_\\____/ \____/   |_|  |______|_____/

 This is where your routes will be defined. Remember they are really just python functions
 that will talk to whatever class you write above. Fast Api simply takes your python results
 and packagres them so they can be sent back to your programs request.
"""


@app.get("/")
async def docs_redirect():
    """Api's base route that displays the information created above in the ApiInfo section."""
    return RedirectResponse(url="/docs")


@app.get("/images/")
async def getImages():
    """
    ### Description:
        Get list of images needing processing
    ### Params:
        None
    ### Returns:
        list : of images
    ## Examples:

    ### Results:
    ```json

    ```
    """
    images = getImageList()
    if images:
        return images
    else:
        return {"Error": "Image directory was empty or a bad path."}


"""
This main block gets run when you invoke this file. How do you invoke this file?

        python api.py 

After it is running, copy paste this into a browser: http://127.0.0.1:8080 

You should see your api's base route!

Note:
    Notice the first param below: api:app 
    The left side (api) is the name of this file (api.py without the extension)
    The right side (app) is the bearingiable name of the FastApi instance declared at the top of the file.
"""
if __name__ == "__main__":
    uvicorn.run("api:app",
                host="127.0.0.1",
                port=8080,
                log_level="debug",
                reload=True)
