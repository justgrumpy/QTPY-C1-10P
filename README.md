# Baby Chopper - QT Py Sound & Animation Project

A fun helicopter toy simulation for the Adafruit QT Py microcontroller featuring realistic sound effects, LED animations, and interactive controls.

## Features

🚁 **Multiple Flight Modes:**
- Startup sequence with engine spin-up sounds
- Flying mode with rotor animations and engine sounds
- Landing mode with reduced power effects
- Emergency mode with alarm sounds and flashing lights

🎵 **Sound Effects:**
- Realistic engine startup and shutdown sequences
- Continuous engine running sounds with variations
- Emergency alarm tones
- All generated using PWM on a simple buzzer

💡 **LED Animations:**
- Rotating rotor blade simulation
- Aircraft navigation lights (red/green/white strobe)
- Progressive startup lighting
- Emergency strobe patterns

🎮 **Interactive Controls:**
- Single button to cycle through all modes
- Visual feedback with onboard LED status
- Automatic mode transitions where appropriate

## Hardware Requirements

### QT Py Board
- Adafruit QT Py RP2040 or SAMD21
- CircuitPython firmware installed

### Components
- **NeoPixel Strip/Ring:** 10 LEDs connected to pin A0
- **Passive Buzzer:** Connected to pin A1  
- **Push Button:** Connected to pin A2 (uses internal pullup)
- **Power:** USB or 3.7V LiPo battery

### Wiring Diagram
```
QT Py Pin    Component
---------    ---------
A0 (D0)  ->  NeoPixel Data In
A1 (D1)  ->  Buzzer Positive
A2 (D2)  ->  Button (one side)
GND      ->  NeoPixel GND, Buzzer GND, Button (other side)
3V       ->  NeoPixel VCC
```

## Installation

1. **Install CircuitPython** on your QT Py:
   - Download from [circuitpython.org](https://circuitpython.org/board/adafruit_qtpy_rp2040/)
   - Copy the UF2 file to the QT Py when in bootloader mode

2. **Install Required Libraries:**
   - Download the [CircuitPython Bundle](https://circuitpython.org/libraries)
   - Copy `adafruit_neopixel.mpy` to the `/lib` folder on your QT Py

3. **Upload the Code:**
   - Copy `code.py` to the root directory of your QT Py
   - The device will automatically restart and begin running

## Usage

1. **Power on** the QT Py (via USB or battery)
2. **Press the button** (A2) to cycle through modes:
   - **OFF** → **STARTUP** → **FLYING** → **LANDING** → **EMERGENCY** → **OFF**
3. **Watch and listen** as the Baby Chopper comes to life!

### Mode Details

- **OFF:** All systems inactive
- **STARTUP:** Engine spin-up sounds with progressive LED lighting
- **FLYING:** Full rotor animation, navigation lights, and engine sounds
- **LANDING:** Slower rotor effects and intermittent engine sounds
- **EMERGENCY:** Flashing red lights with alarm tones

## Customization

### Sound Modifications
Edit the frequency ranges and timing in these methods:
- `startup_sound()` - Engine startup sequence
- `running_sound()` - Continuous flight sounds  
- `emergency_sound()` - Alarm patterns

### Animation Changes
Modify these methods for different LED effects:
- `rotor_animation()` - Spinning blade simulation
- `navigation_lights()` - Aircraft lighting patterns
- `startup_animation()` - Power-up sequence

### Hardware Expansion
The code supports easy addition of:
- Servo motors for physical movement
- Additional LED strips
- Speed control potentiometers
- More buttons for complex controls

## Troubleshooting

**No LEDs lighting up:**
- Check NeoPixel wiring and power
- Verify pin A0 connection
- Try reducing `brightness` value in code

**No sound:**
- Verify buzzer wiring to pin A1
- Check if buzzer is passive (not active)
- Test with different frequency values

**Button not responding:**
- Confirm button wiring to pin A2 and GND
- Check for loose connections
- Button should be normally open

**Code not running:**
- Ensure CircuitPython is properly installed
- Check that `code.py` is in the root directory
- Verify required libraries are in `/lib` folder

## Contributing

Feel free to submit issues, feature requests, or pull requests to enhance the Baby Chopper experience!

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

*Made with ❤️ for makers and helicopter enthusiasts!*