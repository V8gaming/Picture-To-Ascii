import PIL.Image
from PIL import Image
import math
import os
from stringcolor import *
import pathlib
import numpy as np
import shutil

#The characters used for the conversion, it can be added to.
ASCII_CHARS = ["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", ".", " "]

#Interactive inputs
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

#Trys to make the folders if there is none.
try:
    os.mkdir("TempFrames")
except FileExistsError:
    pass
try:
    os.mkdir("Frames")
except FileExistsError:
    pass
try:
    os.mkdir("GifOutput")
except FileExistsError:
    pass

#Gets the file extention of the file inputted.
suffix = str(pathlib.Path(path).suffix)

#Deletes everything in the 'GifOutput' folder.
folder = str(os.getcwd() + "/GifOutput")
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

#Gets all the frames of the gif and splits it up into individual pictures.
#Prints the amount of frames in the file.
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

#When nothing is specified it defaults to 1, same as when its less than 0.
if scale == "":
    scale = 1
if float(scale) < float(0):
    scale = 1

if suffix != ".gif":
    #Stretches & scales the file as long as it's not a gif.
    im = Image.open(path)
    width = im.size[0]
    height = im.size[1] 
    im = im.resize((int(float(width /100 * 165) * float(scale)), int(float(height) * float(scale))), 2)
    im = im.save("Temp.png")
else:
    #Stretches & scales each frame of a gif.
    files = os.listdir("." + "/Frames")
    localpath = str(os.getcwd() + "/Frames/")
    for file in files:
        im = Image.open(localpath + file)
        width = im.size[0]
        height = im.size[1] 
        im = im.resize((int(float(width /100 * 165) * float(scale)), int(float(height) * float(scale))), 2)
        im = im.save("TempFrames/Temp" + file)

#A function to convert the picture to grayscale.
def greyscale(image):
    greyscale_image = image.convert("L")
    return(greyscale_image)

#A function to convert the picture to ascii text.
def pixels_to_ascii(image):
    pixels = image.getdata()
    #Honestly I took this from the tutorial.
    characters = "".join([ASCII_CHARS[pixel//25] for pixel in pixels])
    return(characters)
 
if suffix != ".gif":
    #Converts a the 'Temp' to a text document.
    image = PIL.Image.open("Temp.png")
    innerwidth = int(image.size[0])
    new_image_data = pixels_to_ascii(greyscale(image))
    pixel_count = len(new_image_data)
    ascii_image = "\n".join(new_image_data[i:(i+innerwidth)] for i in range(0, pixel_count, innerwidth))
    print(ascii_image)
    with open("ascii_image.txt", "w") as f:
        f.write(ascii_image)
else:
    #Converts the files in 'TempFrames' to a text document, one for each frame.
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
            #Prints when each frame is rendered/done.
            print("Frame " + str(filenum[b]) + " done.")
            with open("GifOutput/ascii_image"+ str(filenum[b]) +".txt", "w") as f:
                f.write(ascii_image)
        except IndexError:
            pass
        b = b + 1
        image.close()
        im.close()

#Deletes all files 'TempFrames'
foldera = str(os.getcwd() + "/TempFrames")
for filename in os.listdir(foldera):
    file_path = os.path.join(foldera, filename)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

#Deletes all files 'Frames'
folderb = str(os.getcwd() + "/Frames")
for filename in os.listdir(folderb):
    file_path = os.path.join(folderb, filename)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))


#A broken test to turn it to a picture.
#final_data = new_height, new_width, ascii_image
#a = np.asarray(final_data)
#im = Image.fromarray(a)
#im.save("Ascii_png.png")