# piscreenrepo
A little repository for my raspberry pi project.

**What is this?**
I put a piTFT HAT from Adafruit Industries onto a pi zero WH from the same place. This is the repository for the code it uses.
Imagine booting up your Pi and being able to load custom python scripts, using the HAT's joystick and buttons to do everything, removing the need for a keyboard.
This project uses a 240x240 pixel display, and has some utility programs for me to use when I just want to do something like working my DnD clone without using physical dice and such. 
It has a clock, lists the device's stats like CPU usage and temperature, memory usage, disk space, and IP for ssh-ing your way in, virtual dice (d4, d6, d8, d10 and d20, all I need for my RPG), and I plan to add more.

To-Do List:
  - Add pages in the launcher.py list thing
  - Make a calculator app
  - Change up the looks to make them closer to an actual GUI rather than text info:
    - Dice, Clock and Launcher need this. Stats is fine without.

Done:
  - Make a program launcher
  - Make a clock app
  - Make a dice app
  - Re-add the stats app
  - Make the scripts quit/stop when exited.
  - Fixed the issue where the files loaded were not from the repository.
  - Make a pixel art app?
