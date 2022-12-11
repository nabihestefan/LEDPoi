from machine import Pin, Timer, SPI
import neopixel

# COLORS
RED_COLOR = (255, 0, 0)
BLUE_COLOR = (0, 50, 255)
GREEN_COLOR = (0,255,0)
YELLOW_COLOR = (255, 239, 0)

COLORS = [RED_COLOR, GREEN_COLOR, BLUE_COLOR, YELLOW_COLOR]

COLOR_IND = 0

# TIMES
STATIONARY_TIME = 1.6
MOVING_TIME = 0.4

MOVE_THRESHOLD = 250

NUM_PIXELS = 8

# PINS
NEOPIXEL_PIN = Pin(10, Pin.OUT)
BUTTON_PIN = Pin(11, Pin.IN)
LED_PIN = Pin(25, Pin.OUT)

strip = neopixel.NeoPixel(NEOPIXEL_PIN, NUM_PIXELS)

strip.fill(COLORS[COLOR_IND])
strip.write()


mode_button = DigitalInOut(BUTTON_PIN)
mode_button.direction = Direction.INPUT
mode_button.pull = Pull.UP                        

time.sleep(0.1)

# Accelerometer
bus = SPI(0, sck = Pin(18, Pin.OUT), miso = Pin(16, Pin.IN), mosi = Pin(19, Pin.OUT))
# X axis reg 0x08
# X axis reg 0x09
# X axis reg 0x0A

moving = False

# Main program loop, repeats indefinitely
while True:

    if not change.value:                  			# button pressed
        COLOR_IND = (COLOR_IND+1)%len(COLORS) 		# move on to next color
        strip.fill(COLORS[COLOR_IND])            	# Fill and show color on strip              
        strip.show()

    ## This is the accelerometer math (TODO HERE)
#     x, y, z = accel.acceleration # Read accelerometer
#     accel_total = x * x + z * z + y * y
#     
#     if accel_total > MOVE_THRESHOLD:   # Poi is moving
#         COLOR_IND = (COLOR_IND+2)%len(COLORS)
#         time.sleep(0.1)# move on to next color
#         strip.fill(COLORS[COLOR_IND])            	# Fill and show color on strip              
#         strip.show()
#         accel_total = 1
    
