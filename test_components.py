"""
Baby Chopper Test Script
Run this to test individual components before using the main code.
"""

import time
import board
import digitalio
import pwmio
import neopixel

print("Baby Chopper Component Test")
print("=" * 30)

# Test onboard LED
print("Testing onboard LED...")
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

for i in range(5):
    led.value = True
    time.sleep(0.2)
    led.value = False
    time.sleep(0.2)
print("✓ Onboard LED working")

# Test button
print("\nTesting button (A2)...")
button = digitalio.DigitalInOut(board.A2)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

print("Press button within 5 seconds...")
start_time = time.monotonic()
button_pressed = False

while time.monotonic() - start_time < 5.0:
    if not button.value:  # Button pressed (active low)
        print("✓ Button press detected!")
        button_pressed = True
        break
    time.sleep(0.1)

if not button_pressed:
    print("⚠ No button press detected - check wiring")

# Test buzzer
print("\nTesting buzzer (A1)...")
try:
    buzzer = pwmio.PWMOut(board.A1, frequency=440, duty_cycle=0, variable_frequency=True)
    
    # Play test tones
    for freq in [262, 294, 330, 349, 392, 440, 494, 523]:  # C major scale
        buzzer.frequency = freq
        buzzer.duty_cycle = 32768  # 50% duty cycle
        time.sleep(0.2)
        buzzer.duty_cycle = 0
        time.sleep(0.1)
    
    print("✓ Buzzer working - played scale")
    
except Exception as e:
    print(f"⚠ Buzzer error: {e}")

# Test NeoPixels
print("\nTesting NeoPixels (A0)...")
try:
    pixels = neopixel.NeoPixel(board.A0, 10, brightness=0.3, auto_write=False)
    
    # Test basic colors
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255)]
    color_names = ["Red", "Green", "Blue", "White"]
    
    for color, name in zip(colors, color_names):
        print(f"  Showing {name}...")
        pixels.fill(color)
        pixels.show()
        time.sleep(1)
    
    # Animation test
    print("  Running animation test...")
    for step in range(20):
        pixels.fill((0, 0, 0))  # Clear
        pos = step % len(pixels)
        pixels[pos] = (255, 255, 255)
        pixels.show()
        time.sleep(0.1)
    
    pixels.fill((0, 0, 0))  # Clear
    pixels.show()
    print("✓ NeoPixels working - animation complete")
    
except Exception as e:
    print(f"⚠ NeoPixel error: {e}")

print("\nComponent test complete!")
print("If all components are working, you can now run the main code.py file.")