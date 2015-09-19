#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs



import numpy as np

import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import math
from config.no_trend_no_jump import no_trend_no_jump
from config.normal_distribution import normal_distribution
from config.uniform_distribution import uniform_distribution
from config.with_complex_trend_no_jump import with_complex_trend_no_jump
from config.with_trend_no_jump import with_trend_no_jump
import utils.vector
from utils.timer import Timer

timer = Timer()



def generate_data(configs):
    series = []
    for config in configs:
        data = np.zeros(config['data_size'])
        for i in range(0, config['data_size']):
            data[i] = config['function'](i)
        series.append(data)

    data_sum = np.sum(series, axis=0)
    return data_sum, np.range(len(data_sum)), series


def moving_average(data, window_size=20):
    data_size = len(data)

    if window_size == 0:
        return data, np.range(data_size)

    y = np.zeros(data_size)
    for i in range(data_size):
        y[i] = np.sum(data[i:(i + window_size)])
    y /= window_size

    return y[0:-window_size], np.range(window_size, data_size)


data = []
data.append(generate_data(with_trend_no_jump))
data.append(generate_data(no_trend_no_jump))
data.append(generate_data(with_complex_trend_no_jump))
# data.append(generate_data(normal_distribution))
# data.append(generate_data(uniform_distribution))

moving_average_filter_size = 5
filtered_data = []
for x, y, s in data:
    x_, y_ = moving_average(x, moving_average_filter_size)
    filtered_data.append((x_, y_, None))


f, subplots = plt.subplots(2, sharex=True)
subplots[0].grid(True)
subplots[1].grid(True)

# original data
colors = ['r', 'g', 'b', (1, 1, 0)]
for x, y, s in data:
    subplots[0].scatter(y, x, marker='x', c=colors.pop())

# filtered data with moving average filter
colors = ['r', 'g', 'b', (1, 1, 0)]
for x, y, s in filtered_data:
    subplots[1].scatter(y, x, marker='x', c=colors.pop())


plt.figure(1)
f, subplots = plt.subplots(2, len(data), sharex=True)



# histogram of original data
colors = ['r', 'g', 'b', (1, 1, 0)]
i = 0
for x, y, s in data:
    hist, bins = np.histogram(x, bins=20)
    widths = np.diff(bins)
    subplots[0][i].bar(bins[:-1], hist, widths, facecolor=colors.pop())
    i += 1

# histogram of filtered data with moving average filter
colors = ['r', 'g', 'b', (1, 1, 0)]
i = 0
for x, y, s in filtered_data:
    hist, bins = np.histogram(x, bins=20)
    widths = np.diff(bins)
    subplots[1][i].bar(bins[:-1], hist, widths, facecolor=colors.pop())
    i += 1

plt.show()
