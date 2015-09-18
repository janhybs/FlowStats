# encoding: utf-8
# author:   Jan Hybs
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
# import matplotlib.animation as animation
import math
import utils.vector
from utils.timer import Timer

timer = Timer()


# number of elements
data_size = 1000

# mean value and trend change
mean = 0
trend = 50

# noise standard deviation and mean
noise_sigma = 5
noise_mean = 0

# spike standard deviation, mean and probability of spike occurrence
spike_sigma = 20
spike_mean = 0
spike_prob = 0.95


# data without any trend
# data with white/Gaussian noise (constant power spectral density)
no_trend_no_jump = [
    {
        'name': 'data',
        'data_size': data_size,
        'function': lambda i: mean
    },
    {
        'name': 'white-noise',
        'data_size': data_size,
        'function': lambda i: np.random.normal(noise_mean, noise_sigma)
    },
    {
        'name': 'spike-noise',
        'data_size': data_size,
        # with probability of 5% random spike noise will be generated
        'function': lambda i: np.random.normal(spike_mean, spike_sigma) if np.random.random() >= spike_prob else 0.0
    },
]
with_trend_no_jump = [
    {
        'name': 'data',
        'data_size': data_size,
        'function': lambda i: mean + (float(i) / data_size) * trend
    },
    {
        'name': 'white-noise',
        'data_size': data_size,
        'function': lambda i: np.random.normal(noise_mean, noise_sigma)
    },
    {
        'name': 'spike-noise',
        'data_size': data_size,
        # with probability of 5% random spike noise will be generated
        # mean is 0
        # standard deviation is 100
        'function': lambda i: np.random.normal(spike_mean, spike_sigma) if np.random.random() >= spike_prob else 0.0
    },
]
with_complex_trend_no_jump = [
    {
        'name': 'data',
        'data_size': data_size,
        'function': lambda i: mean + trend * math.sin(((float(i) / data_size) * math.pi * 2))
    },
    {
        'name': 'white-noise',
        'data_size': data_size,
        'function': lambda i: np.random.normal(noise_mean, noise_sigma)
    },
    {
        'name': 'spike-noise',
        'data_size': data_size,
        # with probability of 5% random spike noise will be generated
        # mean is 0
        # standard deviation is 100
        'function': lambda i: np.random.normal(spike_mean, spike_sigma) if np.random.random() >= spike_prob else 0.0
    },
]


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


x1, y1, s1 = generate_data(with_trend_no_jump)
x2, y2, s2 = generate_data(no_trend_no_jump)
x3, y3, s3 = generate_data(with_complex_trend_no_jump)

# data_histogram = np.histogram(data, bins=14)
# plt.plot(y1, x1, 'r', y2, x2, 'b', y3, x3, 'g')

moving_average_filter_size = 0
x1, y1 = moving_average(x1, moving_average_filter_size)
x2, y2 = moving_average(x2, moving_average_filter_size)
x3, y3 = moving_average(x3, moving_average_filter_size)

plt.plot(y1, x1, 'r', y2, x2, 'b', y3, x3, 'g')
plt.grid(True)
plt.show()




#
# # uniform distribution: (b - a) * random() + a; sigma = b - a; mu = a
# elem_size = 100
#
# spike_prob = 0.2
# spike_mu = -25
# spike_sigma = 100
#
# mu = -10
# sigma = 20
#
# x = np.ones(elem_size) * mu
# noise = sigma * np.random.random(elem_size)
# spikes = np.array([np.random.random() * spike_sigma + spike_mu if np.random.random() < spike_prob else 0 for i in
# range(0, elem_size)])
#
# y = x + noise + spikes
# t = np.range(elem_size) + 1000
#
# plt.stem(t, y)
# plt.ylabel('f(x)')
# plt.xlabel('x')
# plt.grid(True)
# plt.title(r'Histogram of IQ$\,\sigma_i=15$')
# plt.show()

