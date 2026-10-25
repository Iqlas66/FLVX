import os
import ctypes
import requests
from pathlib import Path


def SET_VVALLPAPER(IMG_PATH):
    SPI_SETDESKWALLPAPER = 20
    SPIF_UPDATEINIFILE = 0x01
    SPIF_SENDCHANGE = 0x02
    abs_path = str(Path(IMG_PATH).resolve())
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER,
        0,
        abs_path,
        SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
    )

def GET_VVALLPAPER_VVALLHAVEN(queries = None):
    FIRST_IMG_PATH = None
    url ="https://wallhaven.cc/api/v1/search"
    output_dir = "wallpapers"
    os.makedirs(output_dir, exist_ok=True)

    for i, query in enumerate(queries):
        params = {
            "q": query,
            "purity": 100,
            "atleast": "1920x1080",
            "sorting": 'random',
            "order": "desc",
            'tag':48189
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            wallpapers = data.get('data', [])
            if wallpapers:
                wp = wallpapers[0]
                IMG_VRL = wp.get('path')
                wp_id  = wp.get('id', f"VVALLPAPER_{i}")
                file_extension =  IMG_VRL.split('.')[-1]
                img_data = requests.get(IMG_VRL, timeout=30).content
                file_path = os.path.join(output_dir, f"{i}_{wp_id}.{file_extension}")
                with open(file_path, 'wb') as handler:
                    handler.write(img_data)

                if FIRST_IMG_PATH is None:
                    FIRST_IMG_PATH = os.path.abspath(file_path)

    if FIRST_IMG_PATH:
        SET_VVALLPAPER(FIRST_IMG_PATH)



