screen_size = (1920, 1024)

planet_offset = 65

screen_color = "#150826"

default_colors=[
    "#F08080",
    "#98FB98",
    "#7FFFD4",
    "#BA55D3",
    "#EE82EE",
    "#FFA07A",
    "#00FF7F",
    "#FFA500"
]

def hex2rgb(hex):
    return tuple(int(hex[1:][i:i+2], 16) for i in (0, 2, 4))

def rgb2hex(rgb):
    return f"#{hex(rgb[0])[2:].zfill(2)}{hex(rgb[1])[2:].zfill(2)}{hex(rgb[2])[2:].zfill(2)}"