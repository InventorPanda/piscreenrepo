import subprocess
import random
import time
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
draw.rectangle((0, 0, width, height), outline=0, fill=(255, 0, 0))
disp.image(image)

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

udlr_fill = "#00FF00"
udlr_outline = "#00FFFF"
button_fill = "#FF00FF"
button_outline = "#FFFFFF"

fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)

indx = 0

diceList = [2, 4, 6, 8, 10, 12, 20]

num  = 0
roll = 0

def constrain(val, minVal, maxVal):
    return min(maxVal, max(minVal, val))

while True:

    draw.rectangle((0, 0, 240, 240), fill=0)

    if not button_U.value:  # up pressed
        indx -= 1

    if not button_D.value:  # down pressed
        indx += 1
        
    indx = constrain(indx, 0, len(diceList)-1)
    num = diceList[indx]

    if not button_A.value:  # roll on A pressed
        roll = random.randint(1, num)
    
    if not button_B.value:  # clear number
        subprocess.run("sudo python3 /home/pi/piscreenrepo/launcher.py", shell=True)
        quit()
    
    rollStr = str(roll) + "/" + str(num)

    draw.text((120, 96), rollStr, font=fnt, fill=udlr_fill)

    y = 24

     for i in range(len(diceList)):

        fillCol = "#00FF00"
        if indx == i:
            fillCol = "#00FFFF"
            draw.rectangle((0, y, 64, y+24), fill=(0, 128, 0))

        draw.text((3, y), "d" + str(diceList[i]), font=fnt, fill=fillCol)
        y += 24

    # Display the Image
    disp.image(image)

    time.sleep(0.1)
