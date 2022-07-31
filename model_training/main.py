import sys, os
sys.path.append(os.getcwd())

from common.model import ArmModel
from common.PID import PID
from common.config import Config
import common.tools as tools 
import numpy as np

config = Config()
pid = PID(config.PID_VAUES['kp'], config.PID_VAUES['ki'], config.PID_VAUES['kd'])
model = ArmModel()
model.fill_model()

training_set = np.genfromtxt(os.path.join(config.DATA_PATH, 'training_data.csv'), delimiter=',', skip_header=1, dtype=np.int16)
normalized = np.interp(training_set, (0, 65535), (0, 1)).astype(np.float32)

data, labels = pid.batch_regulation(normalized[:, 10]), pid.batch_regulation(normalized[:, 2])

train_x_orig, test_x_orig = tools.split_data(data)
train_y_orig, test_y_orig = tools.split_data(labels)

train_x = train_x_orig.reshape((train_x_orig.shape[0], 1, 1))
train_y = train_y_orig.reshape((train_y_orig.shape[0], 1, 1))
test_x = test_x_orig.reshape((test_x_orig.shape[0], 1, 1))
test_y = test_y_orig.reshape((test_y_orig.shape[0], 1, 1))

model.train_model(train_x, test_x, train_y, test_y)
model.save_model()


if False:
    from matplotlib import pyplot as plt

    new_data = normalized[:, 10]
    new_data_smoothed = pid.batch_regulation(new_data)

    predict_test = model.model.predict(np.reshape(new_data_smoothed, (new_data_smoothed.shape[0], 1, 1)))

    plt.title('Model prediction')
    plt.plot(new_data_smoothed, label='EMG')
    plt.plot(predict_test, label='POT')
    plt.legend()
    plt.show()