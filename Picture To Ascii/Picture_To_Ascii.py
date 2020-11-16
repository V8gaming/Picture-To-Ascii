import PIL.Image
from PIL import Image
import math
import os
from stringcolor import *
import pathlib
import numpy as np

ASCII_CHARS = ["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", ".", " "]
def ainput():
    path = input("Input valid path name to image:\n")
    try:
        image = PIL.Image.open(path) 
    except:
        print(path, "Is not a valid path to picture.")
        exit()
    return(path)
path = ainput()

scale = input("Scale 1 is normal(in decimal e.g. 0.5, 1.5 etc), leave empty for normal:\n")

suffix = pathlib.Path(path).suffix

#if suffix == ".gif":
#    im = Image.open(path)
#    try:
#        i = 0
#        frameint = im.n_frames
#        while i <= frameint:
#            a = i + 1
#        frame = list(a)
#        for frame in frames:
#            im.save("Frame"+ str(frame)+".png")
#    except EOFError:
#        pass

if scale == "":
    scale = 1
if int(scale) < 0:
    scale = 1

im = Image.open(path)
width = im.size[0]
height = im.size[1] 

im = im.resize((int(float(width /100 * 165) * float(scale)), int(float(height) * float(scale))), 2)
im = im.save("Temp.png")
im = Image.open("Temp.png")
color = list(im.getdata())
new_width = im.size[0]
new_height = im.size[1]

def greyscale(image):
    greyscale_image = image.convert("L")
    return(greyscale_image)

def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = "".join([ASCII_CHARS[pixel//25] for pixel in pixels])
    return(characters)

def main(innerwidth = int(new_width)):
    image = PIL.Image.open("Temp.png")
    new_image_data = pixels_to_ascii(greyscale(image))

    pixel_count = len(new_image_data)
    ascii_image = "\n".join(new_image_data[i:(i+innerwidth)] for i in range(0, pixel_count, innerwidth))
    im = ascii_image
    print(ascii_image)

    with open("ascii_image.txt", "w") as f:
        f.write(ascii_image)
    #final_data = new_height, new_width, ascii_image
    #a = np.asarray(final_data)
    #im = Image.fromarray(a)
    #im.save("Ascii_png.png")
main()
im.close()
os.remove("Temp.png") 