# Minimal servo controller for testing
import time

class MultiServoController:
    def __init__(self, uart, servos):
        self.uart = uart
        self.servos = servos
        self.config = {
            'servo_channels': [1, 2, 4],
            'switch_channels': [5, 6], 
            'pot_channel': 7,
            'switch_3pos_channel': 8
        }
    
    def update(self):
        pass
    
    def is_connected(self):
        return False
    
    def get_servo_throttle(self, index):
        return 0.0
    
    def get_switch_state(self, switch_num):
        return 0
    
    def get_3pos_switch_state(self):
        return 1
    
    def get_pot_value(self):
        return 50.0
    
    def get_stats(self):
        return {'valid_frames': 0, 'invalid_frames': 0, 'success_rate': 0.0, 'frame_rate': 0.0}
    
    def stop_all_servos(self):
        for servo in self.servos:
            servo.throttle = 0
    
    def set_callbacks(self, switch_cb=None, switch_3pos_cb=None, pot_cb=None, connection_cb=None):
        pass