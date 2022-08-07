from machine import PWM, Pin

class Motor:
    def __init__(self, minimal, maximal, pwm_pin, dirr_pin, initial_dir = True, pwm_freq = 10000):
        self.minimal = minimal
        self.maximal = maximal
        self.pwm_pin = PWM(Pin(pwm_pin))
        self.pwm_pin.freq(pwm_freq)
        self.dirr_pin = Pin(dirr_pin, Pin.OUT)
        self.initial_dir = initial_dir
        self.dirr_pin.value(self.initial_dir)
        
    def change_dir(self):
        self.initial_dir != self.initial_dir
        self.dirr_pin.value(self.initial_dir)

    def set_duty(self, duty):
        self.pwm_pin.duty_u16(duty)