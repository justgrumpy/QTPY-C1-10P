# Multi-Servo Controller - Clear Status Version
import time
import board
import neopixel
import pwmio
import busio
from adafruit_motor import servo
# from servo_controller import MultiServoController

# Initialize LED
led = neopixel.NeoPixel(board.NEOPIXEL, 1)

# Color definitions for better readability
colors = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'purple': (128, 0, 128),
    'orange': (255, 165, 0),
    'yellow': (255, 255, 0),
    'cyan': (0, 255, 255),
    'white': (255, 255, 255),
    'off': (0, 0, 0),
    'light_red': (255, 100, 100),
    'light_green': (100, 255, 100),
    'light_blue': (100, 100, 255)
}

# Quick startup - imports are working fine
led[0] = colors['white']  # White = starting
time.sleep(1)

# Set up UART for RX only
uart = busio.UART(None, board.RX, baudrate=115200, timeout=0.001)

# Test servo creation with PWM-capable pins only
servos = []

# Servo 1 (A2) - PWM capable
try:
    servo1 = servo.ContinuousServo(pwmio.PWMOut(board.A2, frequency=50))
    servos.append(servo1)
    led[0] = colors['red']  # RED = Servo 1 OK
except:
    led[0] = colors['light_red']  # LIGHT RED = Servo 1 FAILED
time.sleep(2)

# Servo 2 (A3) - PWM capable
try:
    servo2 = servo.ContinuousServo(pwmio.PWMOut(board.A3, frequency=50))
    servos.append(servo2)
    led[0] = colors['green']  # GREEN = Servo 2 OK
except:
    led[0] = colors['light_green']  # LIGHT GREEN = Servo 2 FAILED
time.sleep(2)

# Servo 3 (SDA) - PWM capable and close to A2/A3
try:
    servo3 = servo.ContinuousServo(pwmio.PWMOut(board.SDA, frequency=50))
    servos.append(servo3)
    led[0] = colors['blue']  # BLUE = Servo 3 OK
except:
    led[0] = colors['light_blue']  # LIGHT BLUE = Servo 3 FAILED
time.sleep(2)

while True:
    print("forward")
    led[0] = colors['green']
    # servos[0].throttle = 1.0
    time.sleep(4.0)
    print("stop")
    led[0] = colors['red']
    # servos[0].throttle = 0.0
    time.sleep(4.0)
    print("reverse")
    led[0] = colors['purple']
    # servos[0].throttle = -1.0
    time.sleep(4.0)
    print("stop")
    led[0] = colors['red']
    # servos[0].throttle = 0.0
    time.sleep(4.0)
    print("forward")
    led[0] = colors['green']
    # servos[1].throttle = 1.0
    time.sleep(4.0)
    print("stop")
    led[0] = colors['red']
    # servos[1].throttle = 0.0
    time.sleep(4.0)
    print("reverse")
    led[0] = colors['purple']
    # servos[1].throttle = -1.0
    time.sleep(4.0)
    print("stop")
    led[0] = colors['red']
    # servos[1].throttle = 0.0
    time.sleep(4.0)