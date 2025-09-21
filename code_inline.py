# Multi-Servo Controller - Working Version
import time
import board
import neopixel
import pwmio
import busio
from adafruit_motor import servo
from servo_controller import MultiServoController

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

# Set up UART for RX only with better responsiveness
uart = busio.UART(None, board.RX, baudrate=115200, timeout=0.01)

# Create servos
servos = []
servo1 = servo.ContinuousServo(pwmio.PWMOut(board.A2, frequency=50))
servos.append(servo1)
servo2 = servo.ContinuousServo(pwmio.PWMOut(board.A3, frequency=50))
servos.append(servo2)
servo3 = servo.ContinuousServo(pwmio.PWMOut(board.SDA, frequency=50))
servos.append(servo3)

# Create controller
controller = MultiServoController(uart, servos)

# Simple startup indication
led[0] = colors['white']
time.sleep(1)
led[0] = colors['off']

# Main loop with servo control and switch monitoring
# Track previous switch states (channels 5, 6, 8) - start with middle positions
switch_states = [1, 1, 1]

while True:
    # Check for UART data and do basic servo control
    data = uart.read(32)
    if data:
        # Basic iBUS parsing - if we have a full 32-byte frame
        if len(data) == 32 and data[0] == 0x20 and data[1] == 0x40:
            try:
                # Channel 1 -> Servo 1 (A2)
                ch1_raw = (data[3] << 8) | data[2]
                if 800 <= ch1_raw <= 2200:
                    ch1_throttle = (ch1_raw - 1500) / 500.0
                    if abs(ch1_throttle) < 0.02:  # Smaller deadband
                        ch1_throttle = 0.0
                    servo1.throttle = ch1_throttle
                
                # Channel 2 -> Servo 2 (A3)
                ch2_raw = (data[5] << 8) | data[4]
                if 800 <= ch2_raw <= 2200:
                    ch2_throttle = (ch2_raw - 1500) / 500.0
                    if abs(ch2_throttle) < 0.02:  # Smaller deadband
                        ch2_throttle = 0.0
                    servo2.throttle = ch2_throttle
                
                # Channel 4 -> Servo 3 (SDA) - byte positions 8,9
                ch4_raw = (data[9] << 8) | data[8]
                if 800 <= ch4_raw <= 2200:
                    ch4_throttle = (ch4_raw - 1500) / 500.0
                    if abs(ch4_throttle) < 0.02:  # Smaller deadband
                        ch4_throttle = 0.0
                    servo3.throttle = ch4_throttle
                
                # Check Switch 1 (Channel 5) - 2-position - bytes 10,11
                if len(data) > 11:
                    ch5_raw = (data[11] << 8) | data[10]
                    if 800 <= ch5_raw <= 2200:
                        ch5_pos = 0 if ch5_raw < 1500 else 1
                        if ch5_pos != switch_states[0]:
                            switch_states[0] = ch5_pos
                            if ch5_pos == 0:
                                led[0] = colors['purple']  # Low position
                            else:
                                led[0] = colors['orange']  # High position
                            time.sleep(1.0)
                            led[0] = colors['off']  # Turn off after showing switch color
                
                # Check Switch 2 (Channel 6) - 2-position - bytes 12,13
                if len(data) > 13:
                    ch6_raw = (data[13] << 8) | data[12]
                    if 800 <= ch6_raw <= 2200:
                        ch6_pos = 0 if ch6_raw < 1500 else 1
                        if ch6_pos != switch_states[1]:
                            switch_states[1] = ch6_pos
                            if ch6_pos == 0:
                                led[0] = colors['cyan']  # Low position
                            else:
                                led[0] = colors['blue']  # High position
                            time.sleep(1.0)
                            led[0] = colors['off']  # Turn off after showing switch color
                
                # Check Switch 3 (Channel 8) - 3-position - bytes 16,17
                if len(data) > 17:
                    ch8_raw = (data[17] << 8) | data[16]
                    if 800 <= ch8_raw <= 2200:
                        if ch8_raw < 1300:
                            ch8_pos = 0  # Low
                        elif ch8_raw > 1700:
                            ch8_pos = 2  # High
                        else:
                            ch8_pos = 1  # Middle
                        
                        if ch8_pos != switch_states[2]:
                            switch_states[2] = ch8_pos
                            if ch8_pos == 0:
                                led[0] = colors['magenta']  # Magenta - Low
                            elif ch8_pos == 1:
                                led[0] = colors['cyan']  # Cyan - Middle
                            else:
                                led[0] = colors['yellow']  # Yellow - High
                            time.sleep(1.0)
                            led[0] = colors['off']  # Turn off after showing switch color
                
            except:
                pass  # Ignore any parsing errors
    
    controller.update()
    time.sleep(0.05)  # Much faster updates (20Hz)