from machine import Pin, Timer, SPI
import neopixel
import ADXL362 as accel

timer = Timer()

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
STATIONARY_TIME = 1.6
MOVING_TIME = 0.4

MOVE_THRESHOLD = 1

NUM_PIXELS = 8

# PINS
NEOPIXEL_PIN = Pin(10, Pin.OUT)
BUTTON_PIN = Pin(11, Pin.IN)
LED_PIN = Pin(25, Pin.OUT)

strip = neopixel.NeoPixel(NEOPIXEL_PIN, NUM_PIXELS)

strip.fill(COLORS[COLOR_IND][COLOR_SUB_IND])
strip.write()



# mode_button = DigitalInOut(BUTTON_PIN)
# mode_button.direction = Direction.INPUT
# mode_button.pull = Pull.UP                        

# Accelerometer
accel.begin_measure()

# Accelerometer
spi = SPI(0,
          baudrate=1000000,
          polarity=1,
          phase=1,
          bits=8,
          firstbit=machine.SPI.MSB,
          sck=machine.Pin(18),
          mosi=machine.Pin(19),
          miso=machine.Pin(16))

cs = Pin(17, mode=Pin.OUT, value=1)
cs.high()

DEVID = 0xAD
REG_DEVID = 0x00
REG_X     = 0x08
REG_Y     = 0x09
REG_Z     = 0x0A

def reg_read(spi, cs, reg):    
    # Construct message (set ~W bit high)
    msg = bytearray()
    msg.append(0x0B)
    msg.append(reg)
    print(msg)
    
    data = bytearray(1)
    
    # Send out SPI message and read
    cs.low()
    spi.write(msg)

    spi.readinto(data, 0x00)
    cs.high()
    
    print(data)
    return data


def mainChange(timer):
    global COLORS
    global COLOR_IND
    global COLOR_SUB_IND
    COLOR_SUB_IND = (COLOR_SUB_IND+1)%len(COLORS[COLOR_IND])
    strip.fill(COLORS[COLOR_IND][COLOR_SUB_IND])
    strip.write()
    
    
moving = False
timer.init(freq=1, mode=Timer.PERIODIC, callback=mainChange)

reg_read(spi, cs, REG_DEVID)
data = reg_read(spi, cs, REG_DEVID)
if data != bytearray((DEVID, )):
    print("ERROR: Could not communicate with ADXL362")
    sys.exit()

# Main program loop, repeats indefinitely
# while True:
# 
#     if not change.value:                  			# button pressed
#         COLOR_IND = (COLOR_IND+1)%len(COLORS) 		# move on to next color
#         strip.fill(COLORS[COLOR_IND])            	# Fill and show color on strip              
#         strip.show()
# 
#     # Read 3 axes of accelerometer
#     x = reg_read(spi, cs, REG_X)
#     y = reg_read(spi, cs, REG_Y)
#     z = reg_read(spi, cs, REG_Z)

#     x = accel.read_x()
#     y = accel.read_y()
#     z = accel.read_z()

#     print(x, y, z)
#     print(type(x))
# 
#     accel_total = x * x + z * z + y * y
#     
#     if accel_total > MOVE_THRESHOLD and not moving:   # Poi is moving
#         strip.fill(COLORS[GREEN_COLOR])
#         strip.write()
#         timer.deinit()
#         timer.init(freq=4, mode=Timer.PERIODIC, callback=mainChange)
#     elif moving:
#         timer.deinit()
#         timer.init(freq=1, mode=Timer.PERIODIC, callback=mainChange)
    
