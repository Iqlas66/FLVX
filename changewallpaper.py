from pathlib import Path
import datetime
import wallpaper
import  os

def CHANGE_WALLPAPER():
    file = Path("dates.txt")
    today = datetime.date.today()
    with open("dates.txt", 'r') as f:
        dir_path = Path('space')
        z = [n for n in dir_path.iterdir()]
        if str(today) != f.read():
            os.remove(str(z[0].resolve()))
            dir_path = Path('space')
            z = [n for n in dir_path.iterdir()]
            wallpaper.SET_VVALLPAPER(str(z[0].resolve()))
