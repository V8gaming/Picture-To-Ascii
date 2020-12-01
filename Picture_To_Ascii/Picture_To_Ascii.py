from PIL import Image, ImageDraw, ImageFont
from stringcolor import *
import numpy as np
import shutil
from pathlib import Path
import sys
import getopt
import cv2
import threading
from tqdm import tqdm

scale = "null"
framenum = "null"
if any(sys.argv[1:]) == True:
    arguments = sys.argv[2:]
    program_name = sys.argv[0]
    try:
      opts, args = getopt.getopt(arguments,"hs:f:",["scale=","frame="])
    except getopt.GetoptError:
        pass
    for opt, arg in opts:
        if opt == '-h':
            print("For terminal input put(python Picture_To_Ascii (Path) (Arguments)")
            print("Arguements are: -h or --help, -f or --frame, -s or --scale")
            print("(-h)-h or --help prints this text")
            print("(-s)Scales the picture based on a float given eg(1.5 or 0.75 etc) if left empty defaults to 1 or if it is set below 0 defaults to 1")
            print("(-f)Only works if the file is a gif, you can choose which frame to output from (1 to last frame)")
            exit()
        elif opt == '-s' or '--scale':
            scale = arg
        elif opt == '-f' or '--frame':
            framenum = arg
            print(framenum)
    def ainput() -> Path:
        path = str(sys.argv[1])
        return path

#Interactive inputs
elif any(sys.argv[1:]) == False:
    def ainput() -> Path:
        path = input("Input valid path name to supported media:\n")
        path = Path(path) # more flexibility for windows users who wish to use linux "/" slash for their path
        suffix = str(Path(path).suffix)
        try:
            if suffix == ".gif":
                print("If you output as image it will take a while")
            if suffix != ".mp4":
                image = Image.open(path)
            if suffix != ".mov":
                image = Image.open(path)
            if suffix != ".avi":
                image = Image.open(path)
            if suffix != ".mkv":
                image = Image.open(path)
            else:
                pass
        except:
            print(f'{path} is not a valid path to supported media.')
            exit()
        return path


#The characters used for the conversion, it can be added to.
ASCII_CHARS = ["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", ".", " "]

# Initial/entry function to set up the motion
if scale == "null":
    def entry_function() -> tuple[Path, str, float, Path, Path, Path, Path]:
        path = ainput()
        suffix = str(Path(path).suffix)
        #When nothing is specified it defaults to 1, same as when its less than 0.
        scale = input("Scale 1 is normal(in decimal e.g. 0.5, 1.5 etc), leave empty for normal:\n")
        scale = 1 if not scale else float(scale)
        scale = 1 if scale < 0 else scale
        #Trys to make the folders if there are none.
        temp_frames = Path("TempFrames")
        temp_frames.mkdir(exist_ok=True)
        frames_path = Path("Frames")
        frames_path.mkdir(exist_ok=True)
        frame_output = Path("FrameOutput")
        if frame_output.exists():
            shutil.rmtree(frame_output)
        frame_output.mkdir()       
        image_output = Path("ImageOutput")
        if image_output.exists():
            shutil.rmtree(image_output)
        image_output.mkdir()    
        return (path, suffix, scale, 
            temp_frames, frames_path, frame_output, image_output
        )  

    (path, suffix, scale, 
    temp_frames, frames_path, frame_output, image_output) = entry_function()
else:
    def entry_function() -> tuple[Path, str, float, Path, Path, Path]:
        path = ainput()
        suffix = str(Path(path).suffix)
        #Trys to make the folders if there are none.
        temp_frames = Path("TempFrames")
        temp_frames.mkdir(exist_ok=True)
        frames_path = Path("Frames")
        frames_path.mkdir(exist_ok=True)
        frame_output = Path("FrameOutput")
        if frame_output.exists():
            shutil.rmtree(frame_output)
        frame_output.mkdir()
        return (path, suffix, scale, 
            temp_frames, frames_path, frame_output,
        )  

    (path, suffix, scale, 
    temp_frames, frames_path, frame_output,) = entry_function()
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
        frameitr = im.n_frames
        print("Loading")
        with tqdm(range(frameitr)) as pbar:
            for frame in frames:
                im.seek(a)
                im.save("Frames/Frame"+ str(frame)+".png")
                a = a + 1
                pbar.update(1)
    except EOFError:
        pass
    print("Done loading, now stretching")
    with tqdm(range(frameitr)) as abar:
        for file in frames_path.iterdir():
            im = Image.open(file)
            width = im.size[0]
            height = im.size[1] 
            im = im.resize((int(float(width /100 * 165) * float(scale)), int(float(height) * float(scale))), 2)
            new_file = temp_frames / Path("Temp" + file.name)
            im = im.save(new_file)
            abar.update(1)
    #Converts the files in 'TempFrames' to a text document, one for each frame.
    with tqdm(range(frameitr), desc = "Frames Outputted") as bbar:
        for i, file in enumerate(temp_frames.iterdir()):
            with Image.open(file) as im:
                innerwidth = int(im.size[0])
            with Image.open(file) as image:
                new_image_data = pixels_to_ascii(greyscale(image))
            pixel_count = len(new_image_data)
            ascii_image = "\n".join(new_image_data[i:(i+innerwidth)] for i in range(0, pixel_count, innerwidth))
            #Prints when each frame is rendered/done.
            #print("Frame " + str(i) + " done.")
            with (frame_output / f"ascii_image{i}.txt").open("w") as f:
                f.write(ascii_image)
            image.close()
            image = Image.new(mode = "L", size = (int(float(width*8)*float(scale)),int((float(height*8)*float(scale)))), color = "white")
            fnt = ImageFont.truetype('lucon.ttf', 8)
            draw = ImageDraw.Draw(image)
            draw.multiline_text((1,1), ascii_image, font=fnt, spacing = 1, align = "center")
            image = image.resize((int(float(width)*float(scale)), int(float(height)*float(scale))), 2)
            image.save("ImageOutput/"+"Image_output"+ str(i) +".png")
            bbar.update(1)
def video_function():
    video = cv2.VideoCapture(path)
    c = 0
    try:
        vidframes = np.arange(int(video.get(cv2.CAP_PROP_FRAME_COUNT)))
        print("Amount of frames:" + str(int(video.get(cv2.CAP_PROP_FRAME_COUNT))))
        success, image = video.read()
        print("Loading")
        progressitr = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        with tqdm(range(progressitr)) as pbar:
            while success:
                #print(round((c / int(video.get(cv2.CAP_PROP_FRAME_COUNT)) * 100), 2))
                cv2.imwrite("Frames/frame%d.png" % c, image)
                success, image = video.read()
                c += 1
                pbar.update(1)
    except IndexError:
        pass
    print("Done loading, now stretching")
    with tqdm(range(progressitr)) as abar:
        for file in frames_path.iterdir():
            im = Image.open(file)
            width = im.size[0]
            height = im.size[1] 
            im = im.resize((int(float(width /100 * 165) * float(scale)), int(float(height) * float(scale))), 2)
            new_file = temp_frames / Path("Temp" + file.name)
            im = im.save(new_file)
            abar.update(1)
    #Converts the files in 'TempFrames' to a text document, one for each frame.
    with tqdm(range(progressitr), desc = "Frames done") as bbar:
        for i, file in enumerate(temp_frames.iterdir()):
            with Image.open(file) as im:
                innerwidth = int(im.size[0])
            with Image.open(file) as image:
                new_image_data = pixels_to_ascii(greyscale(image))
            pixel_count = len(new_image_data)
            ascii_image = "\n".join(new_image_data[i:(i+innerwidth)] for i in range(0, pixel_count, innerwidth))
            #Prints when each frame is rendered/done.
            with (frame_output / f"ascii_image{i}.txt").open("w") as f:
                f.write(ascii_image)
            bbar.update(1)
            image.close()
        #image = Image.new(mode = "L", size = (width*4,height*4), color = "white")
        #fnt = ImageFont.truetype('lucon.ttf', 8)
        #draw = ImageDraw.Draw(image)
        #draw.multiline_text((1,1), ascii_image, font=fnt, spacing = 1, align = "center")
        #image.save("ImageOutput/"+"Image_output"+ str(i) +".png")
        #image = Image.open("Image_output.png")
        #image = image.resize((int(float(width) * float(scale)), int(float(height) * float(scale))), 2)
        #image.save("Image_output.png")

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
    image = Image.new(mode = "L", size = (int(float(width*8)*float(scale)),int((float(height*8)*float(scale)))), color = "white")
    fnt = ImageFont.truetype('lucon.ttf', 8)
    draw = ImageDraw.Draw(image)
    draw.multiline_text((1,1), ascii_image, font=fnt, spacing = 1, align = "center")
    image = image.resize((int(float(width) * float(scale)), int(float(height) * float(scale))), 2)
    image.save("Image_output.png")

def main():
    if suffix == '.gif':
        gif_function()
    elif suffix == ".mp4":
        video_function()
        #print("If you output as image it will take a while")
    elif suffix == ".mov":
        video_function()
        #print("If you output as image it will take a while")
    elif suffix == ".avi":
        video_function()
        #print("If you output as image it will take a while")
    elif suffix == ".mkv":
        video_function()
        #print("If you output as image it will take a while")
    else:
        non_gif_function()
    #Deletes tempframes and frames folder & files'
    shutil.rmtree(temp_frames)
    shutil.rmtree(frames_path)
if __name__ == '__main__':
    main()