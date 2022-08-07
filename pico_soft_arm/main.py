from machine import UART, ADC, PWM, Pin
from motor import Motor
from PID import PID
import json
import time

analog_pin = 28
analog_channels_start = 2
number_of_analog_channels = 10
pwm_pin = 11
dirr_pin = 10
last_value = 0

pwm = PWM(Pin(pwm_pin))
pwm.freq(10000)

with open('config.json', 'r') as conf:
    config = json.load(conf)

dirr = Pin(dirr_pin, Pin.OUT)
pot_read = ADC(analog_pin)
pot_select_pins = list([Pin(pin_number, Pin.OUT) for pin_number in range(analog_channels_start, analog_channels_start + number_of_analog_channels)])
motors = list([Motor(key["min"], key["max"], key["pwm_min"], key["dirr_pin"]) for key in config])
pid = PID(0.1, 1, 0, 0, 1)
uart = UART(0, 115200)

def map(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    valueScaled = float(value - leftMin) / float(leftSpan)

    return rightMin + (valueScaled * rightSpan)

while True:
    dataset = []
    for current_channel in range(number_of_analog_channels):
        for index, current_pot in enumerate(pot_select_pins):
            current_pot.value(current_channel >> index & 1)
        current_pot_value = map(pot_read.read_u16(), 0, 65355, 0, 1)
        dataset.append('{:.3f}'.format(current_pot_value))
        
    last_value += pid.regulate(eval(dataset[0]), last_value, 0.01)
    
    combined = '{}\n'.format('|'.join(dataset))
    uart.write(combined)
    