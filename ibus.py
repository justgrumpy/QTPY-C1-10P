"""
iBUS Protocol Library - Memory optimized for CircuitPython
Handles iBUS frame parsing and channel value extraction
"""

def extract_channel_value(data, byte_pos):
    """Extract 16-bit channel value from iBUS data"""
    if len(data) > byte_pos + 1:
        return (data[byte_pos + 1] << 8) | data[byte_pos]
    return 1500

def normalize_servo_value(raw_value, deadband=0.02):
    """Convert raw iBUS value to servo throttle (-1.0 to 1.0)"""
    if not (800 <= raw_value <= 2200):
        return 0.0
    throttle = (raw_value - 1500) / 500.0
    return 0.0 if abs(throttle) < deadband else throttle

def get_switch_position(raw_value, is_3pos=False, thresholds=[1300, 1700]):
    """Get switch position from raw iBUS value"""
    if not (800 <= raw_value <= 2200):
        return 0  # Default up position
    
    if is_3pos:
        if raw_value < thresholds[0]:
            return 0  # Low
        elif raw_value > thresholds[1]:
            return 2  # High
        else:
            return 1  # Middle
    else:
        return 0 if raw_value < 1500 else 1

def is_valid_frame(data):
    """Check if iBUS frame is valid"""
    return data and len(data) == 32 and data[0] == 0x20 and data[1] == 0x40

def map_to_volume(raw_value, min_vol=0, max_vol=30):
    """Map iBUS range (1000-2000) to volume range"""
    if 1000 <= raw_value <= 2000:
        return int((raw_value - 1000) * max_vol / 1000)
    return min_vol