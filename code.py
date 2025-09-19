# SPDX-FileCopyrightText: 2019 Anne Barela for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials Servo continuous rotation servo example"""
import time
import board
import neopixel
import pwmio
from adafruit_motor import servo

led = neopixel.NeoPixel(board.NEOPIXEL, 1)  # Change this line
count = .5

colors = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'purple': (128, 0, 128),
    'off': (0, 0, 0)
}

# create a PWMOut object on Pin A2.
pwm = pwmio.PWMOut(board.A2, frequency=50)

# Create a servo object, my_servo.
my_servo = servo.ContinuousServo(pwm)

while True:
    print("forward")
    led[0] = colors['green']
    my_servo.throttle = 1.0
    time.sleep(4.0)
    print("stop")
    led[0] = colors['red']
    my_servo.throttle = 0.0
    time.sleep(4.0)
    print("reverse")
    led[0] = colors['purple']
    my_servo.throttle = -1.0
    time.sleep(4.0)
    print("stop")
    led[0] = colors['red']
    my_servo.throttle = 0.0
    time.sleep(4.0)
