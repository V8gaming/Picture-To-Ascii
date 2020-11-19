import PIL.Image
from PIL import Image
import math
import os
from stringcolor import *
import pathlib
import numpy as np
import shutil

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

suffix = str(pathlib.Path(path).suffix)

folder = str(os.getcwd() + "/GifOutput")
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

if suffix == ".gif":
    im = Image.open(path)
    a = 0
    try:
        print("Amount of frames:" + str(im.n_frames))
        frames = np.arange(im.n_frames)
        for frame in frames:
            im.seek(a)
            im.save("Frames/Frame"+ str(frame)+".png")
            a = a + 1
    except EOFError:
        pass
else:
    pass

if scale == "":
    scale = 1
if float(scale) < float(0):
    scale = 1

if suffix != ".gif":
    im = Image.open(path)
    width = im.size[0]
    height = im.size[1] 
    im = im.resize((int(float(width /100 * 165) * float(scale)), int(float(height) * float(scale))), 2)
    im = im.save("Temp.png")
else:
    files = os.listdir("." + "/Frames")
    localpath = str(os.getcwd() + "/Frames/")
    for file in files:
        im = Image.open(localpath + file)
        width = im.size[0]
        height = im.size[1] 
        im = im.resize((int(float(width /100 * 165) * float(scale)), int(float(height) * float(scale))), 2)
        im = im.save("TempFrames/Temp" + file)

def greyscale(image):
    greyscale_image = image.convert("L")
    return(greyscale_image)

def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = "".join([ASCII_CHARS[pixel//25] for pixel in pixels])
    return(characters)
 
if suffix != ".gif":
    image = PIL.Image.open("Temp.png")
    innerwidth = int(image.size[0])
    new_image_data = pixels_to_ascii(greyscale(image))
    pixel_count = len(new_image_data)
    ascii_image = "\n".join(new_image_data[i:(i+innerwidth)] for i in range(0, pixel_count, innerwidth))
    print(ascii_image)
    with open("ascii_image.txt", "w") as f:
        f.write(ascii_image)

else:
    files = os.listdir("." + "/TempFrames")
    localpath = str(os.getcwd() + "/TempFrames/")
    b = 0
    filenum = np.arange(len(files))
    for file in files:
        im = PIL.Image.open(localpath + file)
        innerwidth = int(im.size[0])
        image = PIL.Image.open(localpath + file)
        new_image_data = pixels_to_ascii(greyscale(image))
        pixel_count = len(new_image_data)
        ascii_image = "\n".join(new_image_data[i:(i+innerwidth)] for i in range(0, pixel_count, innerwidth))
        try:
            print("Frame " + str(filenum[b]) + " done.")
            with open("GifOutput/ascii_image"+ str(filenum[b]) +".txt", "w") as f:
                f.write(ascii_image)
        except IndexError:
            pass
        b = b + 1
        image.close()
        im.close()

foldera = str(os.getcwd() + "/TempFrames")
for filename in os.listdir(foldera):
    file_path = os.path.join(foldera, filename)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

folderb = str(os.getcwd() + "/Frames")
for filename in os.listdir(folderb):
    file_path = os.path.join(folderb, filename)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))




#final_data = new_height, new_width, ascii_image
#a = np.asarray(final_data)
#im = Image.fromarray(a)
#im.save("Ascii_png.png")