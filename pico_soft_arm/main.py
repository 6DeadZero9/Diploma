from machine import UART, ADC
from common.PID import PID
import random 
import time

pid = PID(0.05, 3, 0)
uart = UART(0, 4800)
adc = ADC(28)

def map(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    valueScaled = float(value - leftMin) / float(leftSpan)

    return rightMin + (valueScaled * rightSpan)

while True:
    reading = adc.read_u16()
    mapped = map(reading, 0, 65535, 0, 1)
    print('{:.3f}\n'.format(mapped))
    uart.write('{:.3f}\n'.format(mapped))
    
    
        

