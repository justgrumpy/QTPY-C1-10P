# Multi-Servo Controller - Elegant Inline Version
import time
import board
import neopixel
import pwmio
import busio
from adafruit_motor import servo

# Initialize LED
led = neopixel.NeoPixel(board.NEOPIXEL, 1)

# Color definitions
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

# Configuration
CONFIG = {
    'servo_channels': [1, 2, 4],      # iBUS channels for servos
    'servo_byte_pos': [2, 4, 8],     # Byte positions in iBUS frame
    'switch_channels': [5, 6, 8],    # iBUS channels for switches
    'switch_byte_pos': [10, 12, 16], # Byte positions for switches
    'switch_colors': [
        [colors['purple'], colors['orange']],              # Switch 1: 2-position
        [colors['cyan'], colors['blue']],                  # Switch 2: 2-position  
        [colors['magenta'], colors['cyan'], colors['yellow']] # Switch 3: 3-position
    ],
    'deadband': 0.02,
    'switch_3pos_thresholds': [1300, 1700]  # Low/Middle, Middle/High
}

# Set up UART
uart = busio.UART(None, board.RX, baudrate=115200, timeout=0.01)

# Create servos
servos = [
    servo.ContinuousServo(pwmio.PWMOut(board.A2, frequency=50)),
    servo.ContinuousServo(pwmio.PWMOut(board.A3, frequency=50)),
    servo.ContinuousServo(pwmio.PWMOut(board.SDA, frequency=50))
]

# Helper functions
def extract_channel_value(data, byte_pos):
    """Extract 16-bit channel value from iBUS data"""
    if len(data) > byte_pos + 1:
        return (data[byte_pos + 1] << 8) | data[byte_pos]
    return 1500

def normalize_servo_value(raw_value):
    """Convert raw iBUS value to servo throttle (-1.0 to 1.0)"""
    if not (800 <= raw_value <= 2200):
        return 0.0
    throttle = (raw_value - 1500) / 500.0
    return 0.0 if abs(throttle) < CONFIG['deadband'] else throttle

def get_switch_position(raw_value, is_3pos=False):
    """Get switch position from raw iBUS value"""
    if not (800 <= raw_value <= 2200):
        return 1  # Default middle position
    
    if is_3pos:
        if raw_value < CONFIG['switch_3pos_thresholds'][0]:
            return 0  # Low
        elif raw_value > CONFIG['switch_3pos_thresholds'][1]:
            return 2  # High
        else:
            return 1  # Middle
    else:
        return 0 if raw_value < 1500 else 1

def show_switch_color(switch_idx, position):
    """Display LED color for switch change"""
    color = CONFIG['switch_colors'][switch_idx][position]
    led[0] = color
    time.sleep(1.0)
    led[0] = colors['off']

def update_servos(data):
    """Update all servos from iBUS data"""
    for i, byte_pos in enumerate(CONFIG['servo_byte_pos']):
        if i < len(servos):
            raw_value = extract_channel_value(data, byte_pos)
            servos[i].throttle = normalize_servo_value(raw_value)

def update_switches(data):
    """Update switch states and show LED feedback"""
    for i, byte_pos in enumerate(CONFIG['switch_byte_pos']):
        raw_value = extract_channel_value(data, byte_pos)
        is_3pos = (i == 2)  # Switch 3 is 3-position
        new_position = get_switch_position(raw_value, is_3pos)
        
        if new_position != switch_states[i]:
            switch_states[i] = new_position
            show_switch_color(i, new_position)

def parse_ibus_frame(data):
    """Parse complete iBUS frame and update servos/switches"""
    if not (data and len(data) == 32 and data[0] == 0x20 and data[1] == 0x40):
        return False
    
    try:
        update_servos(data)
        update_switches(data)
        return True
    except:
        return False

# Startup indication
led[0] = colors['white']
time.sleep(1)
led[0] = colors['off']

# Initialize switch states (start with middle positions)
switch_states = [1, 1, 1]

# Main loop - clean and simple!
while True:
    data = uart.read(32)
    if data:
        parse_ibus_frame(data)
    
    time.sleep(0.05)  # 20Hz updates