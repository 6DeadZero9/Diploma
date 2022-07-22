import sys, os
sys.path.append(os.getcwd())

from matplotlib import pyplot as plt
from common.model import ArmModel
from common.PID import PID
import common.tools as tools 
import numpy as np

pid = PID(0.05, 3, 0)
model = ArmModel()
model.load_model()

training_set = np.genfromtxt(os.path.join('data', 'training_data.csv'), delimiter=',', skip_header=1, dtype=np.int16)
normalized = np.interp(training_set, (0, 65535), (0, 1)).astype(np.float32)

smoothed = pid.batch_regulation(normalized[:, 10])

data, labels = smoothed, np.roll(smoothed, 1)

train_x_orig, test_x_orig = tools.split_data(data)
train_y_orig, test_y_orig = tools.split_data(labels)

train_x = train_x_orig.reshape((train_x_orig.shape[0], 1, 1))
train_y = train_y_orig.reshape((train_y_orig.shape[0], 1, 1))
test_x = test_x_orig.reshape((test_x_orig.shape[0], 1, 1))
test_y = test_y_orig.reshape((test_y_orig.shape[0], 1, 1))


new_data = normalized[:, 13]
new_data_smoothed = pid.batch_regulation(new_data)

predict_test = model.model.predict(np.reshape(new_data_smoothed, (new_data_smoothed.shape[0], 1, 1)))

plt.plot(new_data, label='Original data')
plt.plot(new_data_smoothed, label='Smoothed data')
plt.plot(predict_test, label='Predicted data')
plt.plot(pid.batch_regulation(np.reshape(predict_test, (predict_test.shape[0],))), label='Predicted smoothed data')
plt.legend()
plt.show()