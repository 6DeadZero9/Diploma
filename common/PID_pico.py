class PID:
    def __init__(self, kp, ki, kd, bottom_value, top_value, tau = 0.5):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.tau = tau
        self.previous_integration_val = 0
        self.previous_differentiation_val = 0
        self.previous_error = 0
        self.previous_value = 0
        self.bottom_value = bottom_value
        self.top_value = top_value
    
    def regulate(self, wanted_value, current_value, T):
        error = wanted_value - current_value
        proportional = error * self.kp

        self.previous_error = error
        self.previous_integration_val += (self.ki * T * (error + self.previous_error)) / 2

        self.previous_differentiation_val = (2 * self.kd * (current_value - self.previous_value)) / (2 * self.tau  + T) + ((2 * self.tau - T) / (2 * self.tau + T)) * self.previous_differentiation_val
        self.previous_value = current_value

        final_value = (proportional + self.previous_integration_val + self.previous_differentiation_val)
        if self.bottom_value <= current_value + final_value <= self.top_value:
            return final_value
        else:
            return 0
