from colorthief import ColorThief
from io import BytesIO

def getDominantColor(image_bytes):
    color_thief = ColorThief(BytesIO(image_bytes))
    return color_thief.get_color(quality=1)