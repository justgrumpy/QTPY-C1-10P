"""
Baby Chopper Simulator - Test without hardware
This simulates the Baby Chopper experience without requiring actual hardware
Run this on a computer to see the console output simulation
"""

import time
import random

class MockHardware:
    """Mock hardware classes for simulation"""
    
    class MockPixels:
        def __init__(self, pin, count, brightness=0.3, auto_write=False):
            self.count = count
            self.brightness = brightness
            self.pixels = [(0, 0, 0)] * count
            
        def __setitem__(self, index, color):
            if 0 <= index < self.count:
                self.pixels[index] = color
                
        def __getitem__(self, index):
            return self.pixels[index] if 0 <= index < self.count else (0, 0, 0)
            
        def fill(self, color):
            self.pixels = [color] * self.count
            
        def show(self):
            # Print LED status
            led_display = ""
            for i, color in enumerate(self.pixels):
                if color == (0, 0, 0):
                    led_display += "○"  # Off
                elif color == (255, 255, 255):
                    led_display += "●"  # White/bright
                elif color[0] > 0 and color[1] == 0 and color[2] == 0:
                    led_display += "🔴"  # Red
                elif color[0] == 0 and color[1] > 0 and color[2] == 0:
                    led_display += "🟢"  # Green
                else:
                    led_display += "◐"  # Other color
            print(f"LEDs: {led_display}")
    
    class MockBuzzer:
        def __init__(self, pin, frequency=440, duty_cycle=0, variable_frequency=True):
            self.frequency = frequency
            self.duty_cycle = duty_cycle
            
        def play_sound(self, freq, duration):
            if self.duty_cycle > 0:
                sound_desc = "♪" if freq < 300 else "♫" if freq < 600 else "♬"
                print(f"Sound: {sound_desc} {freq}Hz for {duration:.2f}s")
    
    class MockButton:
        def __init__(self):
            self.value = True  # Not pressed
            self.press_count = 0
            
        def check_press(self):
            # Simulate random button presses for demo
            if random.randint(1, 100) == 1:  # 1% chance per check
                self.press_count += 1
                print(f"🔘 Button pressed! (#{self.press_count})")
                return True
            return False
    
    class MockLED:
        def __init__(self):
            self.value = False
            
        def set_value(self, state):
            self.value = state
            status = "🔆" if state else "○"
            print(f"Status LED: {status}")

class BabyChopperSimulator:
    """Simulated Baby Chopper for testing"""
    
    def __init__(self):
        self.pixels = MockHardware.MockPixels("A0", 10)
        self.buzzer = MockHardware.MockBuzzer("A1")
        self.button = MockHardware.MockButton()
        self.led = MockHardware.MockLED()
        
        self.mode = "off"
        self.animation_step = 0
        self.last_update = time.time()
        
        # Color definitions
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.WHITE = (255, 255, 255)
        self.YELLOW = (255, 255, 0)
        self.OFF = (0, 0, 0)
    
    def play_tone(self, frequency, duration=0.1):
        """Simulate playing a tone"""
        self.buzzer.frequency = frequency
        self.buzzer.duty_cycle = 32768 if frequency > 0 else 0
        self.buzzer.play_sound(frequency, duration)
        time.sleep(duration)
        self.buzzer.duty_cycle = 0
    
    def startup_sound(self):
        """Simulate engine startup"""
        print("\n🚁 ENGINE STARTING...")
        for freq in range(100, 500, 50):
            self.play_tone(freq, 0.1)
        print("Engine stabilizing...")
        for _ in range(3):
            self.play_tone(450, 0.1)
            self.play_tone(500, 0.1)
    
    def running_sound(self):
        """Simulate engine running"""
        base_freq = 450 + random.randint(-50, 50)
        self.play_tone(base_freq, 0.05)
    
    def shutdown_sound(self):
        """Simulate engine shutdown"""
        print("\n🚁 ENGINE SHUTTING DOWN...")
        for freq in range(500, 100, -50):
            self.play_tone(freq, 0.1)
    
    def emergency_sound(self):
        """Simulate emergency alarm"""
        print("\n🚨 EMERGENCY MODE!")
        for _ in range(3):
            self.play_tone(800, 0.1)
            self.play_tone(400, 0.1)
    
    def rotor_animation(self):
        """Simulate rotor blade animation"""
        self.pixels.fill(self.OFF)
        
        # Create rotating effect
        num_blades = 3
        for i in range(num_blades):
            blade_pos = (self.animation_step + i * 3) % 10
            self.pixels[blade_pos] = self.WHITE
            prev_pos = (blade_pos - 1) % 10
            self.pixels[prev_pos] = (100, 100, 100)
        
        self.pixels.show()
    
    def navigation_lights(self):
        """Simulate navigation lights"""
        # Red on left, green on right
        if (self.animation_step // 10) % 2:
            self.pixels[0] = self.RED
            self.pixels[9] = self.GREEN
        
        # White strobe
        if (self.animation_step // 20) % 2:
            self.pixels[4] = self.WHITE
            self.pixels[5] = self.WHITE
        
        self.pixels.show()
    
    def startup_animation(self):
        """Simulate startup sequence"""
        progress = (self.animation_step // 5) % 10
        for i in range(progress + 1):
            self.pixels[i] = self.YELLOW
        for i in range(progress + 1, 10):
            self.pixels[i] = self.OFF
        self.pixels.show()
    
    def emergency_animation(self):
        """Simulate emergency strobing"""
        color = self.RED if (self.animation_step // 5) % 2 else self.OFF
        self.pixels.fill(color)
        self.pixels.show()
    
    def change_mode(self):
        """Cycle through modes"""
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
            self.pixels.fill(self.OFF)
            self.pixels.show()
        
        print(f"\n🔄 Mode changed to: {self.mode.upper()}")
    
    def update(self):
        """Main update loop"""
        current_time = time.time()
        
        # Update animation step
        if current_time - self.last_update > 0.1:
            self.animation_step += 1
            self.last_update = current_time
            
            print(f"\rMode: {self.mode.upper()} | Step: {self.animation_step:03d}", end="")
            
            # Handle different modes
            if self.mode == "startup":
                self.startup_animation()
                self.led.set_value((self.animation_step // 5) % 2)
                
                if self.animation_step > 30:  # Auto-advance
                    self.mode = "flying"
                    self.animation_step = 0
                    print(f"\n🔄 Auto-advancing to: {self.mode.upper()}")
                    
            elif self.mode == "flying":
                self.rotor_animation()
                if self.animation_step % 5 == 0:  # Less frequent engine sounds in sim
                    self.running_sound()
                self.led.set_value(True)
                
            elif self.mode == "landing":
                self.rotor_animation()
                if self.animation_step % 10 == 0:  # Even less frequent
                    self.running_sound()
                self.led.set_value((self.animation_step // 10) % 2)
                
            elif self.mode == "emergency":
                self.emergency_animation()
                if self.animation_step % 20 == 0:
                    self.emergency_sound()
                self.led.set_value((self.animation_step // 3) % 2)
                
            else:  # off mode
                self.led.set_value(False)
        
        # Check for button press
        if self.button.check_press():
            self.change_mode()
            self.animation_step = 0

def main():
    print("🚁 Baby Chopper Simulator")
    print("=" * 40)
    print("This simulates the Baby Chopper without hardware")
    print("Watch for automatic button presses and mode changes")
    print("Press Ctrl+C to stop\n")
    
    chopper = BabyChopperSimulator()
    
    try:
        while True:
            chopper.update()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n\n🛑 Simulation stopped")
        print("Upload code.py to your QT Py to run on real hardware!")

if __name__ == "__main__":
    main()