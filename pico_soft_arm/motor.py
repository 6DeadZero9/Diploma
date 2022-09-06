from machine import PWM, Pin

class Motor:
    def __init__(self, minimum, maximum, IA1, IA2, pot_index, emg_index, pwm_freq = 10000):
        self.pot_index = pot_index
        self.emg_index = emg_index
        self.minimum = minimum
        self.maximum = maximum
        self.emg_min = None
        self.emg_max = None
        self.IA1 = PWM(Pin(IA1))
        self.IA2 = PWM(Pin(IA2))
        self.IA1.freq(pwm_freq)
        self.IA2.freq(pwm_freq)
        self.current_value = 0
    
    def set_current_value(self, value):
        if self.minimum <= value <= self.maximum:
            self.current_value = value
        else:
            self.current_value = self.minimum if value <= self.minimum else self.maximum

    def set_duty(self, duty, dirr = True):
        if dirr:
            self.IA1.duty_u16(duty)
            self.IA2.duty_u16(0)
        else:
            self.IA1.duty_u16(0)
            self.IA2.duty_u16(duty)

