# Picture-To-Ascii

## How it works:
It works by using [Pillow](https://pillow.readthedocs.io) to convert your picture to ascii; first by stretching the image's width by +65% because the height of a text character is 65% bigger than the width, it saves that file to "Temp.png". Then it opens that file and converts it to greyscale and ascii text, prints it in console and saves it to "ascii_image.txt". Last it deletes "Temp.png".

## Ideas to work on:
    1. Make it an executible.
    2. Allow GIF files to work. (Done)
    3. More ascii characters.
    4. Output to png, with color choice.
## Stages:
### Stage 1 (Done)
Convert picture to ascii text in full resulution, has scale option.

### Stage 2
Convert picture to ascii text with colour.


## Examples:
The after photo doesn't have colour yet, i think its like an optical illusion or due to my screen resolution.

![Before](d.png)
![After](d_fin.png)

