"""
Baby Chopper with Physical Rotor - Extension Example
This extends the basic Baby Chopper with a servo-controlled rotor
Connect a servo to pin A3 for physical rotor movement
"""

import time
import board
import pwmio
from adafruit_motor import servo

# Import the main Baby Chopper class
from code import BabyChopper, buzzer, pixels, button, onboard_led

class PhysicalChopper(BabyChopper):
    def __init__(self):
        super().__init__()
        
        # Initialize servo for rotor movement
        try:
            pwm = pwmio.PWMOut(board.A3, frequency=50)
            self.rotor_servo = servo.Servo(pwm)
            self.rotor_servo.angle = 90  # Center position
            self.servo_available = True
            print("Servo initialized for physical rotor")
        except:
            self.servo_available = False
            print("Servo not available - continuing without physical rotor")
            
        self.rotor_angle = 90
        self.rotor_speed = 0
    
    def update_physical_rotor(self):
        """Update physical rotor based on mode"""
        if not self.servo_available:
            return
            
        if self.mode == "flying":
            # Fast rotation
            self.rotor_speed = 30
        elif self.mode == "landing":
            # Slower rotation  
            self.rotor_speed = 15
        elif self.mode == "startup":
            # Gradual speed increase
            self.rotor_speed = min(25, self.animation_step // 2)
        else:
            # Stop rotation
            self.rotor_speed = 0
        
        # Update rotor position
        if self.rotor_speed > 0:
            self.rotor_angle += self.rotor_speed
            if self.rotor_angle >= 180:
                self.rotor_angle = 0
            
            # Convert to servo angle (0-180 degrees)
            servo_angle = int(self.rotor_angle)
            self.rotor_servo.angle = servo_angle
    
    def update(self):
        """Override update to include physical rotor"""
        super().update()  # Call parent update method
        self.update_physical_rotor()

# Example usage
def main_with_servo():
    print("Baby Chopper with Physical Rotor starting...")
    print("Connect servo to pin A3 for rotor movement")
    
    chopper = PhysicalChopper()
    
    while True:
        chopper.update()
        time.sleep(0.05)

if __name__ == "__main__":
    main_with_servo()