# Ultra minimal ibus for CircuitPython
import time

class IBusDecoder:
    def __init__(self):
        self.channels = [1500] * 14
    
    def add_byte(self, byte_data):
        return False
    
    def get_channel(self, channel_num):
        if 1 <= channel_num <= 14:
            return self.channels[channel_num - 1]
        return 1500
    
    def normalize_channel(self, channel_num, min_val=-1.0, max_val=1.0):
        return 0.0
    
    def is_connected(self, timeout_ms=100):
        return False
    
    def get_stats(self):
        return {'valid_frames': 0, 'invalid_frames': 0, 'success_rate': 0.0, 'frame_rate': 0.0}
    
    def get_all_channels(self):
        return self.channels
    
    def reset_stats(self):
        pass