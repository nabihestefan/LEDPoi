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
MOVING_FREQ = 4
MOVE_THRESHOLD = 1
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
                        
moving = False
timer.init(freq=STATIONARY_FREQ, mode=Timer.PERIODIC, callback=mainChange)

###############################################################################
# Button   
mode_button = machine.Pin(11, machine.Pin.IN, machine.Pin.PULL_UP)                

###############################################################################
# Accelerometer (not working)
# Assign chip select (CS) pin (and start it high)
cs = machine.Pin(17, machine.Pin.OUT)

# Initialize SPI
spi = machine.SPI(0,
                  baudrate=1000000,
                  polarity=1,
                  phase=1,
                  bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=machine.Pin(18),
                  mosi=machine.Pin(19),
                  miso=machine.Pin(16))

REG_DEVID = 0x00
REG_X = 0x08
REG_Y = 0x09
REG_Z = 0x0A
DEVID = 0xAD

def reg_read(spi, cs, reg):
    
    # Construct message (set ~W bit high)
    msg = bytearray()
    msg.append(0x0B)
    msg.append(reg)
    
    # Send out SPI message and read
    cs.value(0)
    spi.write(msg)
    data = spi.read(1)
    cs.value(1)
    print("REG: ", reg, " MSG: ", msg, " DATA: ", data)
    
    return data

###############################################################################
# Main

# Read device ID to make sure that we can communicate with the ADXL343
# Part below is commented our since accelerometer not working
# Start CS pin high
cs.value(1)

# Workaround: perform throw-away read to make SCK idle high
reg_read(spi, cs, REG_DEVID)
data = reg_read(spi, cs, REG_DEVID)
if (data != bytearray((DEVID,))):
    print("ERROR: Could not communicate with ADXL343")
    sys.exit()


# Main program loop, repeats indefinitely
while True:

    if not mode_button.value():						# button pressed
        COLOR_IND = (COLOR_IND+1)%len(COLORS) 		# move on to next color

    x = reg_read(spi, cs, REG_X)
    y = reg_read(spi, cs, REG_Y)
    z = reg_read(spi, cs, REG_Z)

    accel_total = x * x + z * z + y * y
    
    if accel_total > MOVE_THRESHOLD and not moving:   # Poi is moving
        strip.fill(COLORS[GREEN_COLOR])
        strip.write()
        timer.deinit()
        timer.init(freq=MOVING_FREQ, mode=Timer.PERIODIC, callback=mainChange)
    elif moving:
        timer.deinit()
        timer.init(freq=STATIONARY_FREQ, mode=Timer.PERIODIC, callback=mainChange)

