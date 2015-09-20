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
from config.no_trend_no_jump_with_variation import no_trend_no_jump_with_variation
from config.with_complex_trend_no_jump import with_complex_trend_no_jump
from config.with_trend_no_jump import with_trend_no_jump
from utils.colors import Colors
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
    return data_sum, np.range(len(data_sum))


def moving_average(x, l=20):
    """
    Moving average filter
    :param x:
    :param l: moving average size
    :return: filtered data
    """
    n = len(x)

    if l == 0:
        return x[:]

    y = np.zeros(n)
    for i in range(0, n):
        y[i] = np.sum(x[i:(i + l)])
    y /= l

    return y


def moving_average_complex(x, window=np.hamming(21) / np.sum(np.hamming(21))):
    n = len(x)
    l = len(window)
    if l == 0:
        return x[:]

    # causal filter
    xc = np.append(x[:], np.zeros(l))
    y = np.zeros(n)
    for i in range(0, n):
        y[i] = np.sum(np.multiply(xc[i:i+l], window))

    # # non-causal filter
    # lp = l/2
    # xc = np.append(np.zeros(lp), [x[:], np.zeros(l - lp)])
    # y = np.zeros(n)
    # for i in range(lp, n + lp):
    #     print len (xc[i - lp:i + l - lp]), i - lp, i + l - lp
    #     # y[i] = np.sum(np.multiply(xc[i - l / 2:i + l - l / 2], window))

    return y


def ewma(x, lam=0.1, L=3):
    """
    Exponentially weighted moving average
    :param arr: input array
    :param lam: λ, the weight given to the most recent rational subgroup mean
    :param L: L, the multiple of the rational subgroup standard deviation that establishes the control limits. L is typically set at 3 to match other control charts, but it may be necessary to reduce L slightly for small values of λ
    :return: observations z_i
    """
    n = len(x)
    z = np.zeros(n)

    z[0] = x[0]
    for i in range(1, n):
        z[i] = lam * x[i] + (1 - lam) * z[i - 1]
    return z


colors = Colors(['red', 'blue', 'green', 'red', 'blue', 'green', 'red', 'blue', 'green'])

data = []
ma_data = []
ewma_data = []
# data.append(generate_data(with_trend_no_jump))
# data.append(generate_data(no_trend_no_jump))
data.append(generate_data(with_complex_trend_no_jump))
# data.append(generate_data(no_trend_no_jump_with_variation))
# data.append(generate_data(normal_distribution))
# data.append(generate_data(uniform_distribution))

filter_ma = True
if filter_ma:
    ma_lenght = 10
    for x, y in data:
        x_ = moving_average_complex(x)
        # x_ = x[0:-ma_lenght]
        y_ = np.range(len(x_))
        ma_data.append((x_, y_))

filter_ewma = True
if filter_ewma:
    for x, y in data:
        x_ = ewma(x)
        y_ = y[:]
        ewma_data.append((x_, y_))

plot_data = True
if plot_data:
    f, subplots = plt.subplots(2, sharex=True)
    subplots[0].grid(True)
    subplots[1].grid(True)

    # original data
    colors.reset()
    c = Colors.create(colors.next(), 3)
    for i in range(0, len(data)):
        x, y = data[i]
        x_ma, y_ma = ma_data[i]
        x_ewma, y_ewma = ewma_data[i]
        subplots[0].scatter(y, x, marker='x', c=c.next())
        subplots[0].plot(y_ma, x_ma, c=c.next())
        subplots[0].plot(y_ewma, x_ewma, c=c.next())

        c = Colors.create(colors.next(), 3)

    # filtered data with moving average filter
    colors.reset()
    c = Colors.create(colors.next(), 2)
    for i in range(0, len(data)):
        x_ma, y_ma = ma_data[i]
        x_ewma, y_ewma = ewma_data[i]
        subplots[1].scatter(y_ma, x_ma, marker='x', c=c.next())
        subplots[1].scatter(y_ewma, x_ewma, marker='x', c=c.next())
        c = Colors.create(colors.next(), 2)

plot_histogram = False
if plot_histogram:
    plt.figure(1)
    f, subplots = plt.subplots(2, len(data), sharex=True)

    # histogram of original data
    colors.reset()
    i = 0
    for x, y in data:
        hist, bins = np.histogram(x, bins=20)
        widths = np.diff(bins)
        subplots[0][i].bar(bins[:-1], hist, widths, facecolor=colors.next())
        i += 1

        # histogram of filtered data with moving average filter
        colors.reset()
    i = 0
    for x, y in ma_data:
        hist, bins = np.histogram(x, bins=20)
        widths = np.diff(bins)
        subplots[1][i].bar(bins[:-1], hist, widths, facecolor=colors.next())
        i += 1

plt.show()
