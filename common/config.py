import environ
import os

class Config:
    def __init__(self):
        self.env = environ.Env(
            PID_VALUES=(dict, {
                "kp": 0.05, 
                "ki": 3, 
                "kd": 0
            }),
            DATA_PATH=(str, os.path.join('data')),
            MODEL_PATH=(str, os.path.join('data', 'model.h5'))
        )

        environ.Env.read_env()

        self.PID_VAUES = self.env('PID_VALUES')
        self.DATA_PATH = self.env('DATA_PATH')
        self.MODEL_PATH = self.env('MODEL_PATH')

        
