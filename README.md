# Picture-To-Ascii
***Requires python 3.9***

***Video formats that work are: .mp4, .mov, .avi & .mkv***

***Install: Use gitclone***

## How to run:
    python Picture-To-Ascii.py (path) (arguments)
    -h for help
    -s (in decimal e.g. 0.5, 1.5 etc) for scale
    ps I don't know if these work properly.
## How it works:
It works by using [Pillow](https://pillow.readthedocs.io) to convert your picture to ascii; first by stretching the image's width by +65% because the height of a text character is 65% bigger than the width, it saves that file to "Temp.png". Then it opens that file and converts it to greyscale and ascii text, prints it in console and saves it to "ascii_image.txt". Last it deletes "Temp.png".

## Ideas to work on:
    1. Add arguments to terminal.
    2. Make it use memory instead of temporary files.
    3. Make it an executible.
    4. More ascii characters.
    5. Output to png, with color choice.
    
## Other Additions:
    1. Allow GIF files to work. (Done)
    2. Add docstrings. (continuous)
    3. Added video support(.mp4, .mov, .avi & .mkv) (Done)
## Stages:
### Stage 1 (Done)
Convert picture to ascii text in full resulution, has scale option.

### Stage 2
Convert picture to ascii text with colour.


## Examples:
The after photo doesn't have colour yet, i think its like an optical illusion or due to my screen resolution.

![Before](d.png)
![After](d_fin.png)

