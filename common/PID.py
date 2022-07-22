import numpy as np
import time

class PID:
    def __init__(self, kp, ki, kd, tau = 0.5):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.tau = tau
        self.previous_integration_val = 0
        self.previous_differentiation_val = 0
        self.previous_error = 0
        self.previous_value = 0
    
    def regulate(self, wanted_value, current_value, T):
        error = wanted_value - current_value
        proportional = error * self.kp

        self.previous_error = error
        self.previous_integration_val += (self.ki * T * (error + self.previous_error)) / 2

        self.previous_differentiation_val = (2 * self.kd * (current_value - self.previous_value)) / (2 * self.tau  + T) + ((2 * self.tau - T) / (2 * self.tau + T)) * self.previous_differentiation_val
        self.previous_value = current_value

        return (proportional + self.previous_integration_val + self.previous_differentiation_val)

    def batch_regulation(self, data):
        start_time = time.time()
        last_time = start_time

        new_values = list()
        current_value = data[0]

        for index, step in enumerate(data):
            current_time = time.time()
            dt = current_time - last_time

            control = self.regulate(step, current_value, dt)

            current_value += control
            new_values.append(current_value)
            last_time = current_time
        
        return np.array(new_values)
