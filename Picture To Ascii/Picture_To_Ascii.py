from PIL import Image
from stringcolor import *
import numpy as np
import shutil
from pathlib import Path

#The characters used for the conversion, it can be added to.
ASCII_CHARS = ["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", ".", " "]

#Interactive inputs
def ainput() -> Path:
    path = input("Input valid path name to image:\n")
    path = Path(path) # more flexibility for windows users who wish to use linux "/" slash for their path
    try:
        image = Image.open(path) 
    except:
        print(f'{path} is not a valid path to picture.')
        exit()
    return path

# Initial/entry function to set up the motion
def entry_function() -> tuple[Path, str, float, Path, Path, Path]:
    path = ainput()
    suffix = path.suffix
    #When nothing is specified it defaults to 1, same as when its less than 0.
    scale = input("Scale 1 is normal(in decimal e.g. 0.5, 1.5 etc), leave empty for normal:\n")
    scale = 1 if not scale else float(scale)
    scale = 1 if scale < 0 else scale
    #Trys to make the folders if there are none.
    temp_frames = Path("TempFrames")
    temp_frames.mkdir(exist_ok=True)
    frames_path = Path("Frames")
    frames_path.mkdir(exist_ok=True)
    gif_output = Path("GifOutput")
    if gif_output.exists():
        shutil.rmtree(gif_output)
    gif_output.mkdir()
    return (path, suffix, scale, 
        temp_frames, frames_path, gif_output,
    )  

(path, suffix, scale, 
temp_frames, frames_path, gif_output,) = entry_function()
#A function to convert the picture to grayscale.
def greyscale(image: Image.Image) -> Image.Image:
    greyscale_image = image.convert("L")
    return greyscale_image

#A function to convert the picture to ascii text.
def pixels_to_ascii(image: Image.Image) -> str:
    pixels = image.getdata()
    #Honestly I took this from the tutorial.
    characters = "".join(ASCII_CHARS[pixel//25] for pixel in pixels)
    return characters

def gif_function():
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
    for file in frames_path.iterdir():
        im = Image.open(file)
        width = im.size[0]
        height = im.size[1] 
        im = im.resize((int(float(width /100 * 165) * float(scale)), int(float(height) * float(scale))), 2)
        new_file = temp_frames / Path("Temp" + file.name)
        im = im.save(new_file)
    #Converts the files in 'TempFrames' to a text document, one for each frame.
    for i, file in enumerate(temp_frames.iterdir()):
        with Image.open(file) as im:
            innerwidth = int(im.size[0])
        with Image.open(file) as image:
            new_image_data = pixels_to_ascii(greyscale(image))
        pixel_count = len(new_image_data)
        ascii_image = "\n".join(new_image_data[i:(i+innerwidth)] for i in range(0, pixel_count, innerwidth))
        #Prints when each frame is rendered/done.
        print("Frame " + str(i) + " done.")
        with (gif_output / f"ascii_image{i}.txt").open("w") as f:
            f.write(ascii_image)
        image.close()

def non_gif_function():
    #Stretches & scales the file as long as it's not a gif.
    im = Image.open(path)
    width = im.size[0]
    height = im.size[1] 
    im = im.resize((int(float(width /100 * 165) * float(scale)), int(float(height) * float(scale))), 2)
    im.save("Temp.png")
    image = Image.open("Temp.png")
    innerwidth = int(image.size[0])
    new_image_data = pixels_to_ascii(greyscale(image))
    pixel_count = len(new_image_data)
    ascii_image = "\n".join(new_image_data[i:(i+innerwidth)] for i in range(0, pixel_count, innerwidth))
    print(ascii_image)
    with open("ascii_image.txt", "w") as f:
        f.write(ascii_image)

def main():
    if suffix == '.gif':
        gif_function()
    else:
        non_gif_function()
    #Deletes all files 'TempFrames'
    shutil.rmtree(temp_frames)
    shutil.rmtree(frames_path)

if __name__ == '__main__':
    main()

