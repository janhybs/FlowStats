#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

import numpy as np
import matplotlib.pyplot as plt

from data import filters


class DataConfig(object):
    def __init__(self, size, generator, start=0):
        self.size = size
        self.generator = generator
        self.start = start


def constant_generator(mu=0.0, sigma=1.0):
    def generator(i):
        return np.random.normal(mu, sigma)
    return generator


def linear_generator(scale=1.0, mu=0.0, sigma=1.0):
    def generator(i):
        return i * scale + np.random.normal(mu, sigma)
    return generator


def exponential_generator(scale=1.0, power=2, mu=0.0, sigma=1.0):
    def generator(i):
        return (i ** power) * scale + np.random.normal(mu, sigma)
    return generator


def generate(configs):
    """
    :rtype: numpy.core.multiarray.ndarray
    :type configs: list[DataConfig]
    """
    data = []
    for config in configs:
        config_data = [config.generator(i) for i in range(config.start, config.start + config.size)]
        data.extend(config_data)

    return np.array(range(len(data)), dtype=np.float32), np.array(data, dtype=np.float32)


def plot(data, color, method='scatter', **kwargs):
    getattr(plt, method)(*data, c=color, **kwargs)


scatter_settings = dict(edgecolors='none')
data = generate(
    [
        DataConfig(300, constant_generator(sigma=0.5)),
        DataConfig(300, constant_generator(sigma=2.0)),
        DataConfig(300, exponential_generator(scale=0.0001)),
        DataConfig(300, linear_generator(scale=0.01), start=int(300*300*0.01))
    ]
)

# generate data
sma_data = filters.sma_filter(*data)
maww_data = filters.maww_filter(*data)
ewma_data = filters.ewma_filter(*data)
des_data = filters.des_filter(*data)

# plot data and filtered data
plot(data,      'blue',     'scatter', **scatter_settings)
plot(sma_data,  'red',      'plot')
plot(maww_data, 'green',    'plot')
plot(ewma_data, 'black',    'plot')
plot(des_data,  'brown',    'plot')

# combining filters
des_ewma = filters.combine_filter(filters.des_filter, filters.ewma_filter)
plot(des_ewma(*data), 'pink', 'scatter')

# plot control chart
ucl, lcl = filters.ewma_variance(*data)
plot(ucl, 'purple', 'plot')
plot(lcl, 'purple', 'plot')

# dynamic controls
ducl, dlcl = filters.ewma_adaptive_variance_linear(*data)
plot(ducl, 'orange', 'plot')
plot(dlcl, 'orange', 'plot')

plt.show()

