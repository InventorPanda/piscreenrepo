# Launcher.py, runs at startup.

import subprocess
import time
import random
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
 
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
 
# Clear display.
disp.image(image)
 
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
 
# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)

indx = 0

statsdict = {
    "name": "Stats",
    "command": "sudo python3 /home/pi/stats.py"
}

dicedict = {
    "name": "Dice",
    "command": "sudo python3 /home/pi/dice.py"
}

clockdict = {
    "name": "Clock",
    "command": "sudo python3 /home/pi/clock.py"
}

shutdowndict = {
    "name": "Shutdown",
    "command": "sudo shutdown -h now"
}

rebootdict = {
    "name": "Reboot",
    "command": "sudo reboot"
}


launchlist = [statsdict, clockdict, dicedict, shutdowndict, rebootdict]

top = 12
y = top

print("Starting")

def constrain(val, minVal, maxVal):
    return min(maxVal, max(minVal, val))


while True:

    #Clear the screen
    draw.rectangle((6, top/2, 192, 24*(len(launchlist)+1)), outline="#00FF00", fill=(0, 0, 0))

    y = top

    if not button_U.value:
        indx -= 1
    if not button_D.value:
        indx += 1
        
    indx = constrain(indx, 0, len(launchlist)-1)

    for i in range(len(launchlist)):

        fillCol = "#00FF00"
        if indx == i:
            fillCol = "#FF00FF"

        draw.text((12, y), launchlist[i]["name"], font=fnt, fill=fillCol)
        y += 24

    if not button_A.value:
        cmd = launchlist[indx]["command"]
        subprocess.run(cmd, shell=True)
        quit()
    
    disp.image(image, 180)
    time.sleep(0.1)
