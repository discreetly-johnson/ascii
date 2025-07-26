#This program was heavily inspired by Raphson's on YouTube: https://www.youtube.com/watch?v=2fZBLPk-T2Y&t=1s


'''
The ASCII conversion process rougly involves the following steps:
1.Seperating the image into 2-dimensional array of tiles
2. Applying a scaling factor to reduce the number of pixels used to represent the image, effectively making the characters larger and visible
3. Computing the brightness of each pixels
4. Assigning an ASCII character according to the brightness value
'''

from PIL import Image, ImageDraw, ImageFont
import math

#ascii alphabet taken from GeeksforGeeks at https://www.geeksforgeeks.org/converting-image-ascii-image-python/ 
#alphabet is inverted so that small characters are applied to dark values
ascii_chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~i!lI;:,\"^`'. "[::-1]

charsArray = list(ascii_chars)
charsLength = len(charsArray)

#the program asks for a image file path and opens it
request = input("Please provide a file path for an image to convert")
image = Image.open(request)


#scaleFactor that determines how much to scale down the image
#values are given for the size of the characters so that the image is not squashed/stretched
#a smaller value results in larger pixels (less fidelity)

scaleFactor = float(input("What scaling factor would you like to use (float value)?" \
"For high-resolution images, I recommend 0.01-0.05. Low resolution images" \
"might require a larger value such as 0.2-0.4. Please note that larger values will" \
"require greater processing and file size."))


# this function determines which character is to be used according to the greyscale value that is determined in
#the main function below
interval = charsLength/256
def getCharacters(inputInt):
    return charsArray[math.floor(inputInt*interval)]


#The font here will need to be downloaded and replaced with the required filepath
fonty = ImageFont.truetype('lucon.ttf', 15)


w, h = image.size
#image is resized to prevent warping
#image is scaled down so that ascii characters are visible and not too small
newCharWidth = 10
newCharHeight = 18
image = image.resize((int(scaleFactor*w), int(scaleFactor*h*(newCharWidth/newCharHeight))), Image.NEAREST)
w, h = image.size
pix = image.load()

outputImage = Image.new('RGB', (newCharWidth * w, newCharHeight * h), color = (0,0,0))
d = ImageDraw.Draw(outputImage)

def main():
    for i in range(h):
        for x in range(w):
            r, g, b = pix[x, i]
            greyValue = int(r/3 + g/3 + b/3)
            pix[x, i] = (greyValue,greyValue,greyValue)
        
            d.text((x * newCharWidth, i * newCharHeight), getCharacters(greyValue), font = fonty, fill = (r,g,b))
    
main()

question = str(input("What would you like to name the file?"))
outputImage.save(question+".png")
