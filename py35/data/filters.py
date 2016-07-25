#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

import numpy as np
weighted_hamming = np.hamming(10) / np.sum(np.hamming(10))


def sma_filter(x, y, l=11, trim=False):
    """
    Moving average filter of length l
    :param x:
    :param y:
    :param l:
    :param trim:
    :return:
    """
    n = len(y)
    Y = np.zeros(n)
    for i in range(0, n):
        Y[i] = np.mean(y[i:(i + l)])
    # Y /= l

    if trim:
        return x[:-l], Y[:-l]
    return x, Y


def maww_filter(x, y, window=weighted_hamming, causal=True):
    """
    Moving average with window
    :param y: input data
    :param window: windows which will be used to filter data
    :param causal:
    :return:filtered data
    """
    n = len(y)
    l = len(window)
    if l == 0:
        return y[:]

    # causal filter
    if causal:
        xc = np.append(y[:], np.ones(l) * y[-1])
        Y = np.zeros(n)
        for i in range(0, n):
            Y[i] = np.sum(np.multiply(xc[i:i + l], window))
        return x, Y

    # # non-causal filter
    if not causal:
        lp = l / 2
        xc = np.append(np.zeros(lp), y[:])
        xc = np.append(xc, np.zeros(l - lp))
        Y = np.zeros(n)
        for i in range(lp, n + lp):
            # print len (xc[i - lp:i + l - lp]), i - lp, i + l - lp
            Y[i - lp] = np.sum(np.multiply(xc[i - l / 2:i + l - l / 2], window))

        return x, Y


def ewma_filter(x, y, lam=0.1, L=3):
    """
    Exponentially weighted moving average
    :param y: input data
    :param lam: λ, the weight given to the most recent rational subgroup mean
    :param L: L, the multiple of the rational subgroup standard deviation that establishes the control limits. L is typically set at 3 to match other control charts, but it may be necessary to reduce L slightly for small values of λ
    :return: observations z_i
    """
    n = len(y)
    Y = np.zeros(n)

    Y[0] = y[0]
    for i in range(1, n):
        Y[i] = lam * y[i] + (1 - lam) * Y[i - 1]
    return x, Y


def ewma_filter_pandas(x, y, span=19):
    """
    Exponentially weighted moving average
    :param y: input data
    :param span: center of mass (λ) is calculated as lamda λ = 2/(span + 1), the weight given to the most recent rational subgroup mean
    :return: observations z_i
    """
    import pandas

    return x, pandas.ewma(y, span=span)



def ewma_variance(x, y, lam=0.2, L=3):
    """
    Exponentially weighted moving average control chart
    :param y: input data
    :param lam: λ, the weight given to the most recent rational subgroup mean
    :param L: L, the multiple of the rational subgroup standard deviation that establishes the control limits. L is typically set at 3 to match other control charts, but it may be necessary to reduce L slightly for small values of λ
    :return:
    """
    n = len(y)
    mean = np.mean(y)
    sigma = np.math.sqrt(np.var(y))
    s = np.math.sqrt(lam / (2 - lam))
    ucl = np.ones(n) * (mean + L * s * sigma)
    lcl = np.ones(n) * (mean - L * s * sigma)

    return (x, ucl), (x, lcl)


def ewma_adaptive_variance_linear2(x, y, lam=0.5, L=3, l=50):
    """
    Exponentially weighted moving average adaptive control chart
    :param y: input data
    :param lam: λ, the weight given to the most recent rational subgroup mean
    :param L: L, the multiple of the rational subgroup standard deviation that establishes the control limits. L is typically set at 3 to match other control charts, but it may be necessary to reduce L slightly for small values of λ
    :return:
    """
    n = len(y)
    ucl = np.zeros(n)
    lcl = np.zeros(n)

    i = 0
    ucl[i-1] = np.max(y[0:int(l/2)])
    lcl[i-1] = np.min(y[0:int(l/2)])
    s = np.math.sqrt(lam / (2 - lam))
    for j in range(l, n + l, l):
        mean = np.mean(y[i:j])
        sigma = np.math.sqrt(np.var(y[i:j]))
        ucl_val = mean + L * s * sigma
        lcl_val = mean - L * s * sigma

        ucl[i:j] = np.linspace(ucl[i-1], ucl_val, l)
        lcl[i:j] = np.linspace(lcl[i-1], lcl_val, l)
        i = j

    # ucl = ewmap(ucl)
    # lcl = ewmap(lcl)

    return (x, ucl), (x, lcl)


def ewma_adaptive_variance_linear(x, y, lam=0.5, L=3, l=30):
    i = 0
    n = len(x)

    ucl = np.zeros(n)
    lcl = np.zeros(n)
    while True:
        x_piece = x[i * l:(i + 1) * l]
        y_piece = y[i * l:(i + 1) * l]

        if not len(x_piece):
            break

        _ucl, _lcl = ewma_variance(x_piece, y_piece, lam, L)
        ucl[i * l:(i + 1) * l] = _ucl[1]
        lcl[i * l:(i + 1) * l] = _lcl[1]
        i += 1

    return (x, ucl), (x, lcl)


def des_filter(x, y, alpha=0.1, beta=0.15):
    """
    Double exponential smoothing
    :param y:
    :param alpha: α
    :param beta: β
    :return:
    """
    n = len(y)
    Y = np.zeros(n)
    b = np.zeros(n)

    # first step al
    Y[0] = y[0]
    b[0] = y[1] - y[0]
    b[0] = 0

    for i in range(1, n):
        Y[i] = alpha * y[i] + (1 - alpha) * (Y[i - 1] + b[i - 1])
        b[i] = beta * (Y[i] - Y[i - 1]) + (1 - beta) * b[i - 1]

    return x, Y


def combine_filter(*functions):
    def combine(x, y):
        for function in functions:
            x, y = function(x, y)
        return x, y
    return combine


def outside_bounds(x, y, ucl, lcl):
    x_over = list()
    y_over = list()

    i = 0
    for i in range(len(y)):
        yi = y[i]
        xi = x[i]
        if (yi > ucl[1][i] or yi < lcl[1][i]):
            y_over.append(yi)
            x_over.append(xi)
    return x_over, y_over