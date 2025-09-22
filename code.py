# Multi-Servo Controller - Elegant Inline Version
from time import sleep
import board
from gc import collect
from neopixel import NeoPixel
from pwmio import PWMOut
from busio import UART
from adafruit_motor.servo import ContinuousServo
import dfplayer
import ibus

# Initialize LED
led = NeoPixel(board.NEOPIXEL, 1)

# Set up UART
ibus_uart = UART(None, board.RX, baudrate=115200, timeout=0.01)

# Set up UART for DFPlayer Pro (TX only on D2)
dfplayer_uart = UART(board.D10, None, baudrate=115200)

# Create servos
servos = [
    ContinuousServo(PWMOut(board.A2, frequency=50)),
    ContinuousServo(PWMOut(board.A3, frequency=50)),
    ContinuousServo(PWMOut(board.SDA, frequency=50))
]

# Configuration
CONFIG = {
    'servo_channels': [1, 2, 4],     # iBUS channels for servos
    'servo_byte_pos': [2, 4, 8],     # Byte positions in iBUS frame
    'switch_channels': [5, 6, 8],    # iBUS channels for switches
    'switch_byte_pos': [10, 12, 16], # Byte positions for switches
    'volume_channel': 7,             # iBUS channel for volume POT
    'volume_byte_pos': 14,           # Byte position for volume (channel 7)
    'switch_colors': [
        [(128, 0, 128), (255, 165, 0)],       # purple, orange
        [(0, 255, 255), (0, 0, 255)],         # cyan, blue
        [(255, 0, 255), (0, 255, 255), (255, 255, 0)]  # magenta, cyan, yellow
    ],
    'deadband': 0.02,
    'switch_3pos_thresholds': [1300, 1700]  # Low/Middle, Middle/High
}

# Sound cycling counters
ch5_counter = 0
ch6_counter = 0
current_volume = 8  # Track current volume to avoid unnecessary updates

def show_switch_color(switch_idx, position):
    """Display LED color for switch change and play cycling sounds for channels 5 & 6"""
    global ch5_counter, ch6_counter
    
    color = CONFIG['switch_colors'][switch_idx][position]
    led[0] = color

    # Use direct string literals to save memory
    if switch_idx == 0:  # Channel 5
        sounds = ['tada.mp3', '3wah.mp3', 'exclaim.mp3', 'growl.mp3', 'okay.mp3', 'yes.mp3']
        dfplayer.send_command(dfplayer_uart, 'AT+PLAYFILE=/' + sounds[ch5_counter])
        ch5_counter = (ch5_counter + 1) % 6
    elif switch_idx == 1:  # Channel 6
        sounds = ['grumbl02.mp3', 'grumbl03.mp3', 'grumbl04.mp3', 'grumbl05.mp3']
        dfplayer.send_command(dfplayer_uart, 'AT+PLAYFILE=/' + sounds[ch6_counter])
        ch6_counter = (ch6_counter + 1) % 4

    sleep(1.0)
    led[0] = (0, 0, 0)  # off
    
    # Clean up memory after playing sound
    collect()

def update_volume(data):
    """Update DFPlayer volume based on channel 7 POT position"""
    global current_volume
    
    raw_value = ibus.extract_channel_value(data, CONFIG['volume_byte_pos'])
    new_volume = ibus.map_to_volume(raw_value)
    
    # Only send command if volume changed (to reduce UART traffic)
    if new_volume != current_volume:
        current_volume = new_volume
        dfplayer.send_command(dfplayer_uart, 'AT+VOL=' + str(current_volume))

def update_servos(data):
    """Update all servos from iBUS data"""
    for i, byte_pos in enumerate(CONFIG['servo_byte_pos']):
        if i < len(servos):
            raw_value = ibus.extract_channel_value(data, byte_pos)
            servos[i].throttle = ibus.normalize_servo_value(raw_value, CONFIG['deadband'])

def update_switches(data):
    """Update switch states and show LED feedback"""
    for i, byte_pos in enumerate(CONFIG['switch_byte_pos']):
        raw_value = ibus.extract_channel_value(data, byte_pos)
        is_3pos = (i == 2)  # Switch 3 is 3-position
        new_position = ibus.get_switch_position(raw_value, is_3pos, CONFIG['switch_3pos_thresholds'])
        
        if new_position != switch_states[i]:
            switch_states[i] = new_position
            show_switch_color(i, new_position)

def parse_ibus_frame(data):
    """Parse complete iBUS frame and update servos/switches/volume"""
    if not ibus.is_valid_frame(data):
        return False
    
    try:
        update_servos(data)
        update_switches(data)
        update_volume(data)
        return True
    except:
        return False

# Startup indication
led[0] = (0, 255, 0)  # green
sleep(1)
led[0] = (0, 0, 0)    # off

dfplayer.startup_sequence(dfplayer_uart)

# Initialize switch states (start with up/default positions)
switch_states = [0, 0, 0]

# Final cleanup after initialization
collect()

# Main loop - clean and simple!
loop_counter = 0
while True:
    data = ibus_uart.read(32)
    if data:
        parse_ibus_frame(data)
    
    # Periodic garbage collection every 100 loops (~5 seconds at 20Hz)
    loop_counter += 1
    if loop_counter >= 100:
        collect()
        loop_counter = 0
    
    sleep(0.05)  # 20Hz updates