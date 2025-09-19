"""
Baby Chopper - A fun helicopter toy with sound and animations for Adafruit QT Py
Author: Brian Batronis
License: MIT

This code creates a Baby Chopper experience with:
- LED animations simulating rotor blades and navigation lights
- Sound effects for engine startup, running, and shutdown
- Interactive controls for different modes
"""

import time
import board
import digitalio
import pwmio
import neopixel
import random
from analogio import AnalogIn

# Hardware Configuration for QT Py
# LED strip or NeoPixel for animations (A0/D0)
try:
    pixels = neopixel.NeoPixel(board.A0, 10, brightness=0.3, auto_write=False)
except:
    print("NeoPixel not connected to A0, using onboard LED")
    pixels = None

# Buzzer for sound effects (A1/D1)
try:
    buzzer = pwmio.PWMOut(board.A1, frequency=440, duty_cycle=0, variable_frequency=True)
except:
    print("Buzzer not connected to A1")
    buzzer = None

# Button input (A2/D2) - with internal pullup
button = digitalio.DigitalInOut(board.A2)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# Onboard LED for status
onboard_led = digitalio.DigitalInOut(board.LED)
onboard_led.direction = digitalio.Direction.OUTPUT

# Color definitions
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
OFF = (0, 0, 0)

class BabyChopper:
    def __init__(self):
        self.mode = "off"  # off, startup, flying, landing, emergency
        self.animation_step = 0
        self.last_update = time.monotonic()
        self.button_pressed = False
        self.last_button_state = True
        
    def play_tone(self, frequency, duration=0.1, duty_cycle=32768):
        """Play a tone on the buzzer"""
        if buzzer:
            buzzer.frequency = int(frequency)
            buzzer.duty_cycle = duty_cycle
            time.sleep(duration)
            buzzer.duty_cycle = 0
    
    def startup_sound(self):
        """Engine startup sound sequence"""
        print("Engine starting...")
        # Gradual engine spin-up
        for freq in range(100, 500, 25):
            self.play_tone(freq, 0.05)
        
        # Engine stabilizing
        for _ in range(5):
            self.play_tone(450, 0.1)
            self.play_tone(500, 0.1)
    
    def running_sound(self):
        """Continuous engine running sound"""
        base_freq = 450 + random.randint(-50, 50)
        self.play_tone(base_freq, 0.05, 16384)
    
    def shutdown_sound(self):
        """Engine shutdown sound sequence"""
        print("Engine shutting down...")
        # Engine wind down
        for freq in range(500, 100, -25):
            self.play_tone(freq, 0.08)
    
    def emergency_sound(self):
        """Emergency alarm sound"""
        for _ in range(3):
            self.play_tone(800, 0.1, 32768)
            self.play_tone(400, 0.1, 32768)
    
    def rotor_animation(self):
        """Simulate rotating rotor blades"""
        if not pixels:
            return
            
        # Clear all pixels
        pixels.fill(OFF)
        
        # Create rotating effect with bright white "blades"
        num_blades = 3
        for i in range(num_blades):
            blade_pos = (self.animation_step + i * (len(pixels) // num_blades)) % len(pixels)
            pixels[blade_pos] = WHITE
            # Add trailing effect
            prev_pos = (blade_pos - 1) % len(pixels)
            pixels[prev_pos] = (100, 100, 100)
        
        pixels.show()
    
    def navigation_lights(self):
        """Simulate aircraft navigation lights"""
        if not pixels:
            return
            
        # Red light on left (first pixel)
        pixels[0] = RED if (self.animation_step // 10) % 2 else OFF
        
        # Green light on right (last pixel)
        pixels[-1] = GREEN if (self.animation_step // 10) % 2 else OFF
        
        # White strobe every 2 seconds
        if (self.animation_step // 20) % 2:
            center = len(pixels) // 2
            pixels[center] = WHITE
        
        pixels.show()
    
    def startup_animation(self):
        """LED animation during startup"""
        if not pixels:
            return
            
        # Progressive light-up effect
        progress = (self.animation_step // 5) % len(pixels)
        for i in range(progress + 1):
            pixels[i] = YELLOW
        for i in range(progress + 1, len(pixels)):
            pixels[i] = OFF
        
        pixels.show()
    
    def emergency_animation(self):
        """Flashing red emergency lights"""
        if not pixels:
            return
            
        color = RED if (self.animation_step // 5) % 2 else OFF
        pixels.fill(color)
        pixels.show()
    
    def check_button(self):
        """Check for button press with debouncing"""
        current_state = button.value
        
        if not current_state and self.last_button_state:  # Button pressed
            self.button_pressed = True
        
        self.last_button_state = current_state
        
        if self.button_pressed:
            self.button_pressed = False
            return True
        return False
    
    def change_mode(self):
        """Cycle through different chopper modes"""
        if self.mode == "off":
            self.mode = "startup"
            self.startup_sound()
        elif self.mode == "startup":
            self.mode = "flying"
        elif self.mode == "flying":
            self.mode = "landing"
        elif self.mode == "landing":
            self.mode = "emergency"
            self.emergency_sound()
        else:
            self.mode = "off"
            self.shutdown_sound()
            if pixels:
                pixels.fill(OFF)
                pixels.show()
    
    def update(self):
        """Main update loop"""
        current_time = time.monotonic()
        
        # Update animation step
        if current_time - self.last_update > 0.1:  # 10 FPS
            self.animation_step += 1
            self.last_update = current_time
            
            # Handle different modes
            if self.mode == "startup":
                self.startup_animation()
                onboard_led.value = (self.animation_step // 5) % 2
                
                # Auto-transition to flying after startup sequence
                if self.animation_step > 50:
                    self.mode = "flying"
                    self.animation_step = 0
                    
            elif self.mode == "flying":
                self.rotor_animation()
                self.navigation_lights()
                self.running_sound()
                onboard_led.value = True
                
            elif self.mode == "landing":
                self.rotor_animation()
                # Slower rotor for landing
                if self.animation_step % 2 == 0:
                    self.running_sound()
                onboard_led.value = (self.animation_step // 10) % 2
                
            elif self.mode == "emergency":
                self.emergency_animation()
                if self.animation_step % 20 == 0:
                    self.emergency_sound()
                onboard_led.value = (self.animation_step // 3) % 2
                
            else:  # off mode
                onboard_led.value = False
        
        # Check for button input
        if self.check_button():
            print(f"Mode changing from {self.mode}")
            self.change_mode()
            print(f"Mode changed to {self.mode}")
            self.animation_step = 0

# Main program
def main():
    print("Baby Chopper starting up...")
    print("Press button (A2) to cycle through modes:")
    print("OFF -> STARTUP -> FLYING -> LANDING -> EMERGENCY -> OFF")
    
    chopper = BabyChopper()
    
    # Initial state
    onboard_led.value = True
    time.sleep(0.5)
    onboard_led.value = False
    
    while True:
        chopper.update()
        time.sleep(0.05)  # Small delay to prevent overwhelming the system

if __name__ == "__main__":
    main()