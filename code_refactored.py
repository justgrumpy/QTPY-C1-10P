# Multi-Servo Controller - Clean Version
import time
import board
import neopixel
import pwmio
import busio
from adafruit_motor import servo
from servo_controller import MultiServoController
from ibus import IBusDecoder

# Initialize LED
led = neopixel.NeoPixel(board.NEOPIXEL, 1)

# Color definitions for better readability
colors = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'purple': (128, 0, 128),
    'magenta': (255, 0, 255),
    'orange': (255, 165, 0),
    'yellow': (255, 255, 0),
    'cyan': (0, 255, 255),
    'white': (255, 255, 255),
    'off': (0, 0, 0)
}

# Set up UART for RX only
uart = busio.UART(None, board.RX, baudrate=115200, timeout=0.01)

# Create iBUS decoder
ibus = IBusDecoder()

# Create servos
servos = []
servo1 = servo.ContinuousServo(pwmio.PWMOut(board.A2, frequency=50))
servos.append(servo1)
servo2 = servo.ContinuousServo(pwmio.PWMOut(board.A3, frequency=50))
servos.append(servo2)
servo3 = servo.ContinuousServo(pwmio.PWMOut(board.SDA, frequency=50))
servos.append(servo3)

# Create controller
controller = MultiServoController(uart, servos, ibus)

# LED feedback functions
def on_switch_change(switch_num, position):
    """Handle 2-position switch changes (switches 1 & 2)"""
    if switch_num == 1:  # Switch 1 (Channel 5)
        color = colors['red'] if position == 0 else colors['orange']
    elif switch_num == 2:  # Switch 2 (Channel 6)
        color = colors['cyan'] if position == 0 else colors['blue']
    else:
        return
        
    led[0] = color
    time.sleep(1.0)
    led[0] = colors['off']

def on_3pos_switch_change(position):
    """Handle 3-position switch changes (switch 3)"""
    color_map = {
        0: colors['magenta'],  # Low
        1: colors['green'],     # Middle
        2: colors['yellow']    # High
    }
    
    led[0] = color_map.get(position, colors['white'])
    time.sleep(1.0)
    led[0] = colors['off']

# Set up callbacks
controller.set_callbacks(
    switch_cb=on_switch_change,
    switch_3pos_cb=on_3pos_switch_change
)

# Simple startup indication
led[0] = colors['white']
time.sleep(1)
led[0] = colors['off']

# Main loop - much cleaner now!
while True:
    controller.update()
    time.sleep(0.05)  # 20Hz updates