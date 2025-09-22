# QT Py M0 iBUS Baby Chopper Controller

This project implements a FlySky iBUS receiver for controlling a 3D printed Baby Chopper droid (Mr. Baddeley design) using the Adafruit QT Py M0. The controller manages servo movement and head rotation with sounds and LED feedback for switch positions.

## Project Overview

This code controls a **3D printed Baby Chopper droid** with:
- **Servos 1 & 2**: Differential drive system (tank steering)
- **Servo 3**: Head rotation/spinning
- **LED Feedback**: Visual indication of switch positions
- **DFPlayer Pro**: Sound effects and volume control (via POT)

## Hardware Requirements

### Current Setup:
- **Adafruit QT Py M0** (CircuitPython controller)
- **FlySky transmitter** (e.g., FS-i6, FS-i6X) 
- **FlySky FS-A8S receiver** (iBUS output) - *other FS receivers should work too*
- **3x Continuous rotation servos** (for differential drive + head rotation)
- **DFPlayer Pro** (sound effects module)
- **Speaker** (for droid sounds)
- **Connecting wires**

## Wiring

### QT Py M0 Connections:
- **A7 (RX)**: Connect to receiver iBUS signal output
- **A2**: Servo 1 signal wire (differential drive)
- **A3**: Servo 2 signal wire (differential drive)  
- **SDA**: Servo 3 signal wire (head rotation)
- **D10**: Connect to DFPlayer Pro RX
- **3V**: Receiver power (if using 3.3V receiver)
- **GND**: Common ground
- **Built-in NeoPixel**: Switch position feedback

### FlySky FS-A8S Receiver:
- **iBUS/Sensor port**: Connect signal wire to QT Py A7
- **Power**: Connect to appropriate power source (3.3V or 5V)
- **Ground**: Connect to QT Py GND

### DFPlayer Pro:
- **RX**: Connect to QT Py D10
- **Power**: Connect to appropriate power source (3.3V or 5V)
- **Ground**: Connect to QT Py GND

## Current Implementation

### Active Files:
- **`code.py`**: Main controller, now focused on application logic
  - Imports iBUS and DFPlayer logic from libraries
  - Direct servo control (channels 1, 2, 4)
  - Switch monitoring with LED feedback (channels 5, 6, 8)
  - **DFPlayer Pro sound effects and volume control (channel 7)**
  - Configuration-driven approach for easy customization

- **`lib/ibus.mpy`**: Compiled iBUS protocol library (frame parsing, channel extraction, normalization, etc.)
- **`lib/dfplayer.mpy`**: Compiled DFPlayer Pro library (sound commands, startup sequence)

## Control Mapping

### Servo Channels:
- **Channel 1**: Servo 1 (A2) - Differential drive motor 1
- **Channel 2**: Servo 2 (A3) - Differential drive motor 2  
- **Channel 4**: Servo 3 (SDA) - Head rotation

### Switch Channels:
- **Channel 5**: 2-position switch - Sound effects (DFPlayer Pro, LED feedback)
- **Channel 6**: 2-position switch - Sound effects (DFPlayer Pro, LED feedback)
- **Channel 8**: 3-position switch - Sound effects and animations (currently LED feedback)
- **Channel 7 (POT)**: Volume control for DFPlayer Pro

### Features:
- **DFPlayer Pro**: Plays sound effects on switch triggers, volume set by channel 7 (POT)

## System Architecture

### Data Flow Overview
```mermaid
graph TB
    A[FlySky Transmitter] --> B[FS-A8S Receiver]
    B --> C[iBUS Signal 115200 baud]
    C --> D[QT Py A7 RX Pin]
    D --> E[iBUS Frame Parser]
    E --> F[Channel Extractor]
    F --> G[Servo Controller]
    F --> H[Switch Monitor]
    F --> M[Volume Control - POT]
    H --> I[DFPlayer Pro Sound Trigger]
    M --> J[DFPlayer Pro Volume]
    I --> K[DFPlayer Pro Module]
    J --> K
    K --> L[Speaker]
    G --> N[Servo 1 - A2 Drive Motor 1]
    G --> O[Servo 2 - A3 Drive Motor 2]
    G --> P[Servo 3 - SDA Head Rotation]
    H --> Q[NeoPixel LED Visual Feedback]
```

### iBUS Frame Processing Sequence
```mermaid
sequenceDiagram
    participant TX as Transmitter
    participant RX as FS-A8S Receiver
    participant QT as QT Py M0
    participant Servo as Servos
    participant LED as NeoPixel
    participant DF as DFPlayer Pro
    participant SPK as Speaker
    
    loop Every 20ms
        TX->>RX: Control inputs
        RX->>QT: 32-byte iBUS frame
        
        Note over QT: Frame validation (0x20, 0x40 header)
        
        QT->>QT: Extract channels 1,2,4
        QT->>QT: Normalize to -1.0 to 1.0
        QT->>QT: Apply deadband (±0.02)
        QT->>Servo: Update throttle values
        
        QT->>QT: Extract channels 5,6,8
        QT->>QT: Detect position changes
        
        alt Switch position changed
            QT->>LED: Show color for 1 second
            QT->>DF: Play sound effect
            DF->>SPK: Output sound
            QT->>LED: Turn off
        end
        
        QT->>QT: Extract channel 7 (POT)
        QT->>DF: Set volume
    end
```

### Switch State Machine
```mermaid
stateDiagram-v2
    [*] --> Reading
    Reading --> Checking: Extract raw value
    Checking --> Changed: Position differs
    Checking --> Reading: Same position
    Changed --> LEDDisplay: Show color
    Changed --> Sound: Play sound (DFPlayer Pro)
    LEDDisplay --> LEDOff: After 1 second
    LEDOff --> Reading
    Sound --> Reading
    
    state "2-Position Switch Logic" as TwoPos {
        [*] --> Low
        Low --> High: Value > 1500
        High --> Low: Value < 1500
    }
    
    state "3-Position Switch Logic" as ThreePos {
        [*] --> Middle
        Middle --> Low: Value < 1300
        Middle --> High: Value > 1700
        Low --> Middle: Value > 1300
        High --> Middle: Value < 1700
    }
```

## Library Structure and Memory Optimization

To maximize available RAM and keep `code.py` clean:
- **iBUS protocol code** is in `lib/ibus.mpy` (compiled from `ibus.py`)
- **DFPlayer Pro code** is in `lib/dfplayer.mpy` (compiled from `dfplayer.py`)
- **All configuration and main loop logic** remain in `code.py`
- **No unused imports or global dictionaries** (e.g., colors are now direct tuples)
- **Garbage collection (`collect()`)** is used strategically to free memory

This structure allows for larger features and more reliable operation on memory-constrained boards like the QT Py M0.

### Helper Functions (now in libraries):
- **`ibus.extract_channel_value()`**: Get raw values from iBUS frame
- **`ibus.normalize_servo_value()`**: Convert to servo throttle with deadband
- **`ibus.get_switch_position()`**: Handle 2 and 3-position switches
- **`ibus.is_valid_frame()`**: Validate iBUS frame
- **`ibus.map_to_volume()`**: Map POT value to DFPlayer volume
- **`dfplayer.send_command()`**: Send AT command to DFPlayer Pro
- **`dfplayer.startup_sequence()`**: Initialize DFPlayer Pro

### Application Functions (in `code.py`):
- **`show_switch_color()`**: LED feedback and sound cycling
- **`update_servos()`**: Process all servos in loop
- **`update_switches()`**: Handle switch monitoring
- **`update_volume()`**: Handle volume changes
- **`parse_ibus_frame()`**: Main frame processing

### Main Loop:
```python
loop_counter = 0
while True:
    data = uart.read(32)
    if data:
        parse_ibus_frame(data)
    # Periodic garbage collection every 100 loops (~5 seconds at 20Hz)
    loop_counter += 1
    if loop_counter >= 100:
        collect()
        loop_counter = 0
    sleep(0.05)  # 20Hz updates
```
- Reads iBUS data, updates servos, switches, and volume.
- Triggers sound effects and LED feedback on switch changes.
- Periodically runs garbage collection to free memory.

## LED Status Indicators

The built-in NeoPixel currently provides feedback for switch positions *(will be replaced with sound effects and animations)*:

### Switch 1 (Channel 5) - 2 Position:
- **Purple**: Position 0 (Low) - *Future: Sound effect trigger*
- **Orange**: Position 1 (High) - *Future: Different sound effect*

### Switch 2 (Channel 6) - 2 Position:  
- **Cyan**: Position 0 (Low) - *Future: Animation trigger*
- **Blue**: Position 1 (High) - *Future: Different animation*

### Switch 3 (Channel 8) - 3 Position:
- **Magenta**: Position 0 (Low) - *Future: Animation mode 1*
- **Cyan**: Position 1 (Middle) - *Future: Animation mode 2*
- **Yellow**: Position 2 (High) - *Future: Animation mode 3*

### Startup:
- **Green**: System starting up

## Baby Chopper Droid Control

### Tank Steering System:
The Baby Chopper uses **differential drive** (tank steering) where channels 1 and 2 are mixed to create:

#### Forward/Backward Movement:
- **Both motors same direction**: Droid moves forward or backward
- **Channel 1 & 2 receive same throttle values**

#### Rotational Movement:
- **Motors opposite directions**: Droid spins in place
- **Right turn**: Channel 1 forward + Channel 2 reverse → Clockwise spin
- **Left turn**: Channel 1 reverse + Channel 2 forward → Counter-clockwise spin

#### Mixed Movement:
- **Differential speeds**: Curved movement paths
- **One motor faster**: Droid curves toward slower motor side

### Movement Control:
- **Forward Stick**: Both drive motors forward (droid moves forward)
- **Backward Stick**: Both drive motors reverse (droid moves backward)
- **Right Stick**: Motors rotate opposite directions (droid spins clockwise)
- **Left Stick**: Motors rotate opposite directions (droid spins counter-clockwise)
- **Head Control**: Right stick vertical controls head rotation speed (channel 4)
- **Deadband**: 2% around center to prevent drift

### Switch Functions (Current):
- **Switches 1 & 2**: LED feedback only and sound effect triggers
- **Switch 3**: LED feedback only (will become animation mode selection)

### Sound ###
- **Sound Effects**: DFPlayer Pro integration with switch triggers
- **Volume Control**: POT channel for audio levels

### Future Enhancements:
- **Animations**: Pre-programmed movement and sound sequences triggered by switches
- **LED Replacement**: Switch LED feedback replaced with sound/movement responses

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
    """Extract 16-bit channel value from iBUS frame"""
    if len(data) > byte_pos + 1:
        return (data[byte_pos + 1] << 8) | data[byte_pos]
    return 1500
```

## Usage Example

### Basic Setup:
```python
# Create servos for Baby Chopper
servos = [
    servo.ContinuousServo(pwmio.PWMOut(board.A2, frequency=50)),  # Drive motor 1
    servo.ContinuousServo(pwmio.PWMOut(board.A3, frequency=50)),  # Drive motor 2  
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

### Pin Selection:
- **A0, A1**: Cannot do PWM (used A2, A3, SDA instead)
- **A7**: RX pin for iBUS data
- **TX**: Did not work for DFPlayer Pro communication
- **D10**: Works for DFDlayer Pro communication

## Future Roadmap

### Phase 1 (Current):
- ✅ Basic servo control
- ✅ Switch monitoring with LED feedback
- ✅ Elegant inline code structure

### Phase 2 (Current):
- 🔄 DFPlayer Pro integration  
- 🔄 POT volume control
- 🔄 Replace LED feedback with sound effects

### Phase 3 (Planned):
- 📋 Switch-triggered animations
- 📋 Pre-programmed movement animations
- 📋 Coordinated movement + sound sequences
- 📋 Baby Chopper personality behaviors

## License

MIT License - See individual file headers for details.