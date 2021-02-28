# Template file for making new apps.

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
 
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
 
# Clear display.
disp.image(image)
 
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
 
# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)

while True:

    #Clear the screen
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Here's where your code would go

    if not button_B.value:  # Quit after going back to the launcher
        subprocess.run("sudo python3 /home/pi/piscreenrepo/launcher.py", shell=True)
        quit()
    
    disp.image(image)
    time.sleep(0.1)
