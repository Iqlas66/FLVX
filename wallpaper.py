import os
import ctypes
import requests
from pathlib import Path


def SET_VVALLPAPER(IMG_PATH):
    """"
    Sets the desktop wallpaper to the image specified by IMG_PATH
    using the Win32 SystemParametersInfoW API.
    """
    SPI_SETDESKWALLPAPER = 20
    SPIF_UPDATEINIFILE = 0x01
    SPIF_SENDCHANGE = 0x02

    #Resolve to absolute path
    abs_path = str(Path(IMG_PATH).resolve())

    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER,
        0,
        abs_path,
        SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
    )

def GET_VVALLPAPER_VVALLHAVEN(queries = None):
    """
           Queries the Wallhaven API for each search term in the list, downloads
           the top matching wallpaper, saves them to a local 'wallpapers' directory,
           and sets the very first downloaded image as the active desktop background.
       """

    FIRST_IMG_PATH = None
    url ="https://wallhaven.cc/api/v1/search"
    output_dir = "wallpapers"
    os.makedirs(output_dir, exist_ok=True)

    headers = {
        "User-Agent": "FLVX-Borderland-App/1.0"  #Header so Wallhaven doesnt give 403
    }


    for i, query in enumerate(queries):
        params = {
            "q": query,
            "purity": 100, #SFW
            "atleast": "1920x1080",
            "sorting": 'random',
            "order": "desc",

        }

        response = requests.get(url, params=params,headers=headers)  #Gets  a response with params and a header

        if response.status_code == 200:
            data = response.json()
            wallpapers = data.get('data', [])

            if wallpapers:
                wp = wallpapers[0]
                img_url = wp.get('path')
                wp_id  = wp.get('id', f"VVALLPAPER_{i}")
                #Removes params so it creates a working file extension
                file_extension =  img_url.split('?')[0].split('.')[-1]
                #Adds a timeout of 30s  so it doesnt loop infinitely
                img_data = requests.get(img_url, timeout=30, headers=headers).content
                file_path = os.path.join(output_dir, f"{i}_{wp_id}.{file_extension}")
                with open(file_path, 'wb') as handler:
                    handler.write(img_data) # Writes the image bytes

                if FIRST_IMG_PATH is None:
                    FIRST_IMG_PATH = os.path.abspath(file_path)

    if FIRST_IMG_PATH:
        SET_VVALLPAPER(FIRST_IMG_PATH) #If images are downloaded then applies the wallpapers


