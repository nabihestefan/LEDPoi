from machine import Pin, Timer, SPI
import neopixel
import sys

timer = Timer()

###############################################################################
# LEDS

# COLORS
RED = (255, 0, 0)
BLUE = (0, 50, 255)
GREEN = (0,255,0)
YELLOW = (255, 239, 0)
WHITE = (255, 255, 255)

COLORS = [[WHITE],
          [RED, WHITE],
          [BLUE,WHITE],
          [GREEN,WHITE],
          [YELLOW,WHITE],
          [RED,BLUE],
          [BLUE,GREEN],
          [BLUE,YELLOW],
          [RED, BLUE, GREEN]]

COLOR_IND = -1
COLOR_SUB_IND=0

# TIMES
STATIONARY_FREQ = 2
NUM_PIXELS = 8

# PINS
NEOPIXEL_PIN = Pin(10, Pin.OUT)
LED_PIN = Pin(25, Pin.OUT)

# Strip setup
strip = neopixel.NeoPixel(NEOPIXEL_PIN, NUM_PIXELS)
strip.fill(COLORS[COLOR_IND][COLOR_SUB_IND])
strip.write()

def mainChange(timer):
    global COLORS
    global COLOR_IND
    global COLOR_SUB_IND
    COLOR_SUB_IND = (COLOR_SUB_IND+1)%len(COLORS[COLOR_IND])
    strip.fill(COLORS[COLOR_IND][COLOR_SUB_IND])
    strip.write()
              
timer.init(freq=STATIONARY_FREQ, mode=Timer.PERIODIC, callback=mainChange)

###############################################################################
# Button   
mode_button = machine.Pin(11, machine.Pin.IN, machine.Pin.PULL_UP)                

###############################################################################
# Main program loop, repeats indefinitely
while True:

    if not mode_button.value():						# button pressed
        COLOR_IND = (COLOR_IND+1)%len(COLORS) 		# move on to next color
        while not mode_button.value():				# Filler code to wait until button is released
            a = 1
        
