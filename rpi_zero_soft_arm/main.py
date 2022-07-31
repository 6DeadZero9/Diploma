import sys, os
sys.path.append(os.getcwd())

from common.config import Config
from common.PID import PID
import serial
import time

ser = serial.Serial('/dev/serial0',
    baudrate = 115200,
    timeout=0.01
)
config = Config()
pid = PID(config.PID_VAUES['kp'], config.PID_VAUES['ki'], config.PID_VAUES['kd'], 0, 1)
last_value = 0
last_time = time.time()

while True:
    current_time = time.time()
    dt = current_time - last_time

    try:
        line = ser.readline()
        if line: 
            stripped = eval(line.rstrip())
            if 0 <= stripped <= 1:
                last_value += pid.regulate(stripped, last_value, dt)
                print(last_value)

                ser.write(str.encode('{:.3f}\n'.format(stripped)))
    except Exception as error:
        pass
    
    last_time = current_time