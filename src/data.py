# encoding: utf-8
# author:   Jan Hybs
import numpy as np

np.random.seed(1234)
def generate_data(configs):
    series = []
    for config in configs:
        data = np.zeros(config['data_size'])
        for i in range(0, config['data_size']):
            data[i] = config['function'](i)
        series.append(data)

    data_sum = np.sum(series, axis=0)
    return data_sum, np.range(len(data_sum))