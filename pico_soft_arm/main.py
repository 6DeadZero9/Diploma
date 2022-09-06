from machine import UART, ADC, PWM, Pin
from motor import Motor
import json
import time

analog_pin = 28
adc = ADC(27)
analog_channels_start = 2
number_of_analog_channels = 10

min_speed = 20000
max_speed = 65535

with open('config.json', 'r') as conf:
    config = json.load(conf)

pot_read = ADC(analog_pin)
pot_select_pins = list([Pin(pin_number, Pin.OUT) for pin_number in range(analog_channels_start, analog_channels_start + 4)])
motors = {key: Motor(config[key]["min"],
                     config[key]["max"],
                     config[key]["IA1"],
                     config[key]["IA2"],
                     config[key]["pot_index"],
                     config[key]["emg_index"],) for key in config}

def map_values(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    valueScaled = float(value - leftMin) / float(leftSpan)

    return rightMin + (valueScaled * rightSpan)

while True:
    dataset = []
    for current_channel in range(number_of_analog_channels):
        for index, current_pot in enumerate(pot_select_pins):
            current_pot.value(current_channel >> index & 1)
        current_pot_value = pot_read.read_u16()
        dataset.append(current_pot_value)
        
    reading = adc.read_u16()
     
    for current_motor in motors:
        motors[current_motor].set_current_value(dataset[motors[current_motor].pot_index])
        #reading = dataset[motors[current_motor].emg_index]
        
        if motors[current_motor].emg_min is None or reading < motors[current_motor].emg_min:
            motors[current_motor].emg_min = reading
        if motors[current_motor].emg_max is None or reading > motors[current_motor].emg_max:
            motors[current_motor].emg_max = reading
            
        try:
            goal_mapped = int(map_values(reading, motors[current_motor].emg_min, motors[current_motor].emg_max,
                                         motors[current_motor].minimum, motors[current_motor].maximum))
            diff = goal_mapped - motors[current_motor].current_value
            diff_sign = diff >= 0
            diff = abs(diff)
            diff_mapped = int(map_values(motors[current_motor].minimum + diff, motors[current_motor].minimum,
                                         motors[current_motor].maximum, min_speed, max_speed))
            motors[current_motor].set_duty(diff_mapped, diff_sign)
        except Exception as error:
            pass

    time.sleep(0.1)
    
