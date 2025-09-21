# QT Py M0 iBUS Baby Chopper Controller

This project implements a FlySky iBUS receiver for controlling a 3D printed Baby Chopper droid (Mr. Baddeley design) using the Adafruit QT Py M0. The controller manages servo movement and head rotation with LED feedback for switch positions.

## Project Overview

This code controls a **3D printed Baby Chopper droid** with:
- **Servos 1 & 2**: Droid movement (left/right wheels or tracks)
- **Servo 3**: Head rotation/spinning
- **LED Feedback**: Visual indication of switch positions
- **Future Features**: DFPlayer Pro for sound effects and animations

## Hardware Requirements

### Current Setup:
- **Adafruit QT Py M0** (CircuitPython controller)
- **FlySky transmitter** (e.g., FS-i6, FS-i6X) 
- **FlySky FS-A8S receiver** (iBUS output) - *other FS receivers should work too*
- **3x Continuous rotation servos** (for droid movement + head)
- **Connecting wires**

### Future Additions:
- **DFPlayer Pro** (sound effects module)
- **Speaker** (for droid sounds)
- **Additional switches** (for pre-programmed animations)

## Wiring

### QT Py M0 Connections:
- **A7 (RX)**: Connect to receiver iBUS signal output
- **A2**: Servo 1 signal wire (left movement)
- **A3**: Servo 2 signal wire (right movement)  
- **SDA**: Servo 3 signal wire (head rotation)
- **3V**: Receiver power (if using 3.3V receiver)
- **GND**: Common ground
- **Built-in NeoPixel**: Switch position feedback

### FlySky FS-A8S Receiver:
- **iBUS/Sensor port**: Connect signal wire to QT Py A7
- **Power**: Connect to appropriate power source (3.3V or 5V)
- **Ground**: Connect to QT Py GND

## Current Implementation

### Active Files:
- **`code.py`**: Main controller with inline iBUS parsing
  - Elegant, refactored design with helper functions
  - Direct servo control (channels 1, 2, 4)
  - Switch monitoring with LED feedback (channels 5, 6, 8)
  - Configuration-driven approach for easy customization

### Inactive Files (For Reference):
- **`lib/ibus.py`**: Minimal placeholder library
- **`lib/servo_controller.py`**: Minimal placeholder library  
- **`code_*.py`**: Alternative implementations (not currently used)

*Note: We learned that CircuitPython on QT Py M0 works best with simpler, inline approaches rather than complex library structures.*

## Control Mapping

### Servo Channels:
- **Channel 1**: Servo 1 (A2) - Left movement
- **Channel 2**: Servo 2 (A3) - Right movement  
- **Channel 4**: Servo 3 (SDA) - Head rotation

### Switch Channels:
- **Channel 5**: 2-position switch - Purple/Orange LED feedback
- **Channel 6**: 2-position switch - Cyan/Blue LED feedback
- **Channel 8**: 3-position switch - Magenta/Cyan/Yellow LED feedback

### Future Planned:
- **POT Channel**: Volume control for DFPlayer Pro
- **Additional Switches**: Pre-programmed animation triggers
- **Sound Integration**: Coordinated movement and sound effects

## Code Structure

The current implementation uses a **clean, inline approach** in `code.py` with these key features:

### Configuration-Driven Design:
```python
CONFIG = {
    'servo_channels': [1, 2, 4],      # iBUS channels for servos
    'servo_byte_pos': [2, 4, 8],     # Byte positions in iBUS frame
    'switch_channels': [5, 6, 8],    # iBUS channels for switches
    'switch_colors': [
        [colors['purple'], colors['orange']],              # Switch 1: 2-position
        [colors['cyan'], colors['blue']],                  # Switch 2: 2-position  
        [colors['magenta'], colors['cyan'], colors['yellow']] # Switch 3: 3-position
    ],
    'deadband': 0.02,
    'switch_3pos_thresholds': [1300, 1700]
}
```

### Helper Functions:
- **`extract_channel_value()`**: Get raw values from iBUS frame
- **`normalize_servo_value()`**: Convert to servo throttle with deadband
- **`get_switch_position()`**: Handle 2 and 3-position switches
- **`show_switch_color()`**: LED feedback system
- **`update_servos()`**: Process all servos in loop
- **`update_switches()`**: Handle switch monitoring
- **`parse_ibus_frame()`**: Main frame processing

### Main Loop:
```python
while True:
    data = uart.read(32)
    if data:
        parse_ibus_frame(data)
    controller.update()  # Compatibility placeholder
    time.sleep(0.05)  # 20Hz updates
```

## LED Status Indicators

The built-in NeoPixel provides feedback for switch positions:

### Switch 1 (Channel 5) - 2 Position:
- **Purple**: Position 0 (Low)
- **Orange**: Position 1 (High)

### Switch 2 (Channel 6) - 2 Position:  
- **Cyan**: Position 0 (Low)
- **Blue**: Position 1 (High)

### Switch 3 (Channel 8) - 3 Position:
- **Magenta**: Position 0 (Low)
- **Cyan**: Position 1 (Middle)  
- **Yellow**: Position 2 (High)

### Startup:
- **White**: System starting up

## Baby Chopper Droid Control

### Movement Control:
- **Left Stick Horizontal**: Differential steering (channels 1 & 2)
- **Right Stick Vertical**: Head rotation speed (channel 4)
- **Deadband**: 2% around center to prevent drift

### Switch Functions (Current):
- **Switches 1 & 2**: Visual feedback only (future animation triggers)
- **Switch 3**: Visual feedback only (future mode selection)

### Future Enhancements:
- **Sound Effects**: DFPlayer Pro integration
- **Animations**: Pre-programmed movement sequences
- **Volume Control**: POT channel for audio levels
- **Sound Triggers**: Switch-activated droid sounds

## iBUS Protocol Implementation

- **Baud Rate**: 115200 bps
- **Frame Size**: 32 bytes  
- **Update Rate**: ~50Hz (20ms)
- **Channels**: 14 channels, 16-bit each
- **Range**: Typically 1000-2000 microseconds

### Frame Format:
```
[0x20] [0x40] [Ch1_L] [Ch1_H] [Ch2_L] [Ch2_H] ... [Ch14_L] [Ch14_H] [CRC_L] [CRC_H]
```

### Channel Data Extraction:
```python
def extract_channel_value(data, byte_pos):
    """Extract 16-bit channel value from iBUS data"""
    if len(data) > byte_pos + 1:
        return (data[byte_pos + 1] << 8) | data[byte_pos]
    return 1500
```

## Usage Example

### Basic Setup:
```python
# Create servos for Baby Chopper
servos = [
    servo.ContinuousServo(pwmio.PWMOut(board.A2, frequency=50)),  # Left movement
    servo.ContinuousServo(pwmio.PWMOut(board.A3, frequency=50)),  # Right movement  
    servo.ContinuousServo(pwmio.PWMOut(board.SDA, frequency=50))  # Head rotation
]

# Main control loop
while True:
    data = uart.read(32)
    if data:
        parse_ibus_frame(data)  # Updates servos and switches
    time.sleep(0.05)  # 20Hz updates
```

### Servo Control:
```python
def normalize_servo_value(raw_value):
    """Convert raw iBUS value to servo throttle (-1.0 to 1.0)"""
    if not (800 <= raw_value <= 2200):
        return 0.0
    throttle = (raw_value - 1500) / 500.0
    return 0.0 if abs(throttle) < CONFIG['deadband'] else throttle
```

## Troubleshooting

### No Connection:
1. Check wiring between FS-A8S receiver and QT Py A7
2. Verify receiver is bound to transmitter
3. Ensure receiver is powered  
4. Check baud rate (should be 115200)
5. Look for white LED startup indication

### Servos Not Responding:
1. Verify servos are connected to A2, A3, SDA
2. Check servo power requirements
3. Ensure channels 1, 2, 4 are active on transmitter
4. Check for LED feedback when moving switches

### Switch LED Not Working:
1. Move switches on channels 5, 6, 8
2. Verify transmitter switch assignments
3. Check for 1-second color display followed by LED off
4. Ensure magenta color is now defined in colors dictionary

## Development Notes

### Why Inline Implementation?
We discovered that CircuitPython on QT Py M0 works best with simpler approaches:
- **Complex libraries cause import crashes** and yellow error blinks
- **Inline code is more reliable** and easier to debug
- **Memory constraints** favor monolithic design
- **Direct hardware access** provides better performance

### Pin Selection:
- **A0, A1**: Cannot do PWM (used A2, A3, SDA instead)
- **A7**: RX pin for iBUS data
- **TX**: Reserved for future DFPlayer Pro communication

## Future Roadmap

### Phase 1 (Current):
- ✅ Basic servo control
- ✅ Switch monitoring with LED feedback
- ✅ Elegant inline code structure

### Phase 2 (Planned):
- 🔄 DFPlayer Pro integration
- 🔄 POT volume control
- 🔄 Switch-triggered sound effects

### Phase 3 (Future):
- 📋 Pre-programmed movement animations
- 📋 Coordinated movement + sound sequences
- 📋 Baby Chopper personality behaviors

## License

MIT License - See individual file headers for details.