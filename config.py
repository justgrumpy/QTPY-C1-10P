"""
Baby Chopper Configuration
Customize these settings for different hardware setups or preferences
"""

# LED Configuration
NUM_PIXELS = 10          # Number of NeoPixels in your strip/ring
LED_BRIGHTNESS = 0.3     # LED brightness (0.1 to 1.0)
LED_PIN = "A0"          # Pin for NeoPixel data

# Sound Configuration  
BUZZER_PIN = "A1"       # Pin for buzzer
ENGINE_BASE_FREQ = 450  # Base frequency for engine sound (Hz)
ENGINE_VARIATION = 50   # Frequency variation for realistic engine sound
STARTUP_FREQ_MIN = 100  # Starting frequency for engine startup
STARTUP_FREQ_MAX = 500  # Ending frequency for engine startup

# Control Configuration
BUTTON_PIN = "A2"       # Pin for mode button
ANIMATION_FPS = 10      # Animation frames per second
UPDATE_DELAY = 0.05     # Main loop delay (seconds)

# Animation Timing
STARTUP_DURATION = 50   # Animation steps for startup sequence
ROTOR_BLADES = 3        # Number of rotor blades to simulate
STROBE_RATE = 20        # Animation steps between navigation strobe

# Sound Durations (seconds)
TONE_DURATION = 0.1     # Standard tone length
STARTUP_STEP_DURATION = 0.05  # Duration of each startup frequency step
EMERGENCY_BEEP_DURATION = 0.1  # Emergency alarm beep length

# Color Definitions (R, G, B)
COLORS = {
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255),
    'WHITE': (255, 255, 255),
    'YELLOW': (255, 255, 0),
    'PURPLE': (255, 0, 255),
    'CYAN': (0, 255, 255),
    'OFF': (0, 0, 0),
    'DIM_WHITE': (100, 100, 100),
    'ORANGE': (255, 165, 0)
}

# Mode-specific settings
MODES = {
    'off': {
        'led_pattern': 'solid',
        'led_color': 'OFF',
        'sound_enabled': False
    },
    'startup': {
        'led_pattern': 'progressive',
        'led_color': 'YELLOW',
        'sound_enabled': True,
        'auto_advance': True,
        'auto_advance_delay': 50
    },
    'flying': {
        'led_pattern': 'rotor_nav',
        'led_color': 'WHITE',
        'sound_enabled': True,
        'engine_sound': True
    },
    'landing': {
        'led_pattern': 'rotor_nav',
        'led_color': 'WHITE', 
        'sound_enabled': True,
        'engine_sound': True,
        'engine_intermittent': True
    },
    'emergency': {
        'led_pattern': 'strobe',
        'led_color': 'RED',
        'sound_enabled': True,
        'alarm_sound': True
    }
}