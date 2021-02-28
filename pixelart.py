# A Pixel ARt application. Kind of difficult, I think.

import time
import subprocess
from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
 
# Create the display
cs_pin = DigitalInOut(board.CE0)
dc_pin = DigitalInOut(board.D25)
reset_pin = DigitalInOut(board.D24)
BAUDRATE = 24000000
 
spi = board.SPI()
disp = st7789.ST7789(
    spi,
    height=240,
    y_offset=80,
    rotation=180,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)
 
# Input pins:
button_A = DigitalInOut(board.D5)
button_A.direction = Direction.INPUT
 
button_B = DigitalInOut(board.D6)
button_B.direction = Direction.INPUT
 
button_L = DigitalInOut(board.D27)
button_L.direction = Direction.INPUT
 
button_R = DigitalInOut(board.D23)
button_R.direction = Direction.INPUT
 
button_U = DigitalInOut(board.D17)
button_U.direction = Direction.INPUT
 
button_D = DigitalInOut(board.D22)
button_D.direction = Direction.INPUT
 
button_C = DigitalInOut(board.D4)
button_C.direction = Direction.INPUT
 
# Turn on the Backlight
backlight = DigitalInOut(board.D26)
backlight.switch_to_output()
backlight.value = True
 
# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for color.
width = disp.width
height = disp.height
image = Image.new("RGB", (width, height))
imgOverlay = Image.new("RGBA", (width, height))

pixelWidth = width/32
pixelHeight = width/32
pixelSize = 32

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
drawOnTop = ImageDraw.Draw(imgOverlay)
 
# Clear display.
disp.image(image)
disp.image(imgOverlay)
 
# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
smolFont = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)

cursorX = 0
cursorY = 0

cursorColIndx = 0

menuIndx = 1
showMenu = False

colorList = [(0, 0, 0), (128, 128, 128), (255, 255, 255), (255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0),
             (0, 255, 0), (0, 128, 0), (0, 255, 128), (0, 255, 255), (0, 128, 255), (0, 0, 255), (0, 0, 128), 
             (128, 0, 128), (128, 0, 255), (255, 0, 255), (255, 0, 128)]

def constrain(val, minVal, maxVal):
    return min(maxVal, max(minVal, val))

while True:

    #Clear the screen
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    if not showMenu:
        if not button_R.value:
            cursorX ++
        if not button_L.value:
            cursorX --
        if not button_U.value:
            cursorY --
        if not button_D.value:
            cursorY ++
      cursorX = constrain(cursorX, 0, pixelSize)
      cursorY = constrain(cursorY, 0, pixelSize)

    if not button_A.value: # Add a pixel to the image.
        drawOnTop.rectangle((cursorX * pixelWidth, cursorY * pixelHeight, (cursorX+1)*pixelWidth, (cursorY+1)*pixelHeight), fill=colorList[cursorColIndx])
    
    if not button_B.value:  # Pull up the menu
        if showMenu == True:
            showMenu = False
        else:
            showMenu = True
        
    if showMenu == True:
            # display the menu
            draw.rectangle((0, 196, width, height), outline=(64, 64, 64), fill=(192, 192, 192))
            draw.rectangle((80, 208, 120, 226), outline=(248, 250, 255), fill=colorList[cursorColIndx])
            draw.text((140, 208), "save", font=smolFont, fill=0)
            draw.text((200, 208), "quit" , font=smolFont, fill=0)
            
            #use the menu
            if not button_R.value:
                menuIndx += 1
                menuIndx = constrain(menuIndx, 0, 2)
            if not button_L.value:
                menuIndx -= 1
                menuIndx = constrain(indx, 0, 2)
            if not button_A.value:
                if menuIndx == 2:
                    subprocess.run("sudo python3 /home/pi/piscreenrepo/launcher.py", shell=True) # Quit after going back to the launcher
                    quit()
                else if menuIndx == 1:
                    imgOverlay.save("image.png")
                else if menuIndx == 0:
                    cursorColIndx += 1
                    cursorColIndx = constrain(cursorColIndx, 0, len(colorList)-1)

    disp.image(image)
    disp.image(imgOverlay)
    time.sleep(0.1)
