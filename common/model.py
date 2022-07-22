from tensorflow import keras
from tensorflow.keras import layers
import os

class ArmModel:
    def __init__(self) -> None:
        self.model = None

    def fill_model(self): 
        self.model = keras.Sequential()
        self.model.add(layers.LSTM(256, input_shape=(1, 1)))
        self.model.add(layers.Dropout(0.4))
        self.model.add(layers.Dense(1))

        self.model.compile(
            loss='mean_squared_error',
            optimizer="adam"
        )

    def train_model(self, train_x, test_x, train_y, test_y, save_model=True):
        if self.model is not None:
            self.model.fit(
                train_x, train_y, validation_data=(test_x, test_y), batch_size=15, epochs=10
            )
        else:
            print("Model is not initialized")

    def save_model(self, path = os.path.join('data', 'model')):
        if self.model is not None:
            self.model.save_weights(path)
        else:
            print("Model is not initialized")

    def load_model(self, path = os.path.join('data', 'model')):
        self.fill_model()
        self.model.load_weights(path)