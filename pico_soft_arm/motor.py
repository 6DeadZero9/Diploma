from machine import PWM, Pin

class Motor:
    def __init__(self, minimal, maximal, pwm_pin, dirr_pin, initial_dirr = True, pwm_freq = 10000):
        self.minimal = minimal
        self.maximal = maximal
        self.pwm_pin = PWM(Pin(pwm_pin))
        self.pwm_pin.freq(pwm_freq)
        self.initial_dirr = initial_dirr
        self.current_dirr = initial_dirr
        self.dirr_pin = Pin(dirr_pin, Pin.OUT)
        self.dirr_pin.value(self.current_dirr)
        
    def change_dir(self):
        self.current_dirr != self.current_dirr
        self.dirr_pin.value(self.current_dirr)

    def set_duty(self, duty):
        self.pwm_pin.duty_u16(duty)