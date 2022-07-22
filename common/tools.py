import numpy as np 

def split_data(data, split_ration = 0.8):
    array_size = data.shape[0]

    return data[:int(array_size * split_ration)], data[int(array_size * split_ration):]