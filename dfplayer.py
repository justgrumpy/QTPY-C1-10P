from time import sleep
from gc import collect

def send_command(uart, command):
    uart.write(f'{command}\r\n')

def startup_sequence(uart):
    """Initialize DFPlayer Pro with startup settings"""
    sleep(3)
    
    # LED and prompt stick until they are specifically changed
    # Configure DFPlayer settings
    # dfplayer_send_command('AT+LED=OFF')      # Turn off LED indicator
    # sleep(0.5)
    
    # dfplayer_send_command('AT+PROMPT=OFF')      # Turn off LED indicator
    # sleep(0.5)

    send_command(uart, 'AT+PLAYMODE=3')   # Play one song and pause
    sleep(0.5)
    
    # Play startup file (file #1)
    send_command(uart, 'AT+PLAYFILE=/startup.mp3')    # Play startup sound
    sleep(0.5)
    
    # Clean up memory after startup
    collect()