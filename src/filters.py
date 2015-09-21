# encoding: utf-8
# author:   Jan Hybs
import math
import numpy as np


def sma(x, l=11, trim_x=False):
    """
    Moving average filter
    :param x: input data
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

    if trim_x:
        return y[0:-l]
    return y


weighted_hamming = np.hamming(11) / np.sum(np.hamming(11))


def maww(x, window=weighted_hamming, causal=False):
    """
    Moving average with window
    :param x: input data
    :param window: windows which will be used to filter data
    :param causal:
    :return:filtered data
    """
    n = len(x)
    l = len(window)
    if l == 0:
        return x[:]

    # causal filter
    if causal:
        xc = np.append(x[:], np.zeros(l))
        y = np.zeros(n)
        for i in range(0, n):
            y[i] = np.sum(np.multiply(xc[i:i + l], window))
        return y

    # # non-causal filter
    if not causal:
        lp = l / 2
        xc = np.append(np.zeros(lp), x[:])
        xc = np.append(xc, np.zeros(l - lp))
        y = np.zeros(n)
        for i in range(lp, n + lp):
            # print len (xc[i - lp:i + l - lp]), i - lp, i + l - lp
            y[i - lp] = np.sum(np.multiply(xc[i - l / 2:i + l - l / 2], window))

        return y


def ewma(x, lam=0.1, L=3):
    """
    Exponentially weighted moving average
    :param x: input data
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


def ewma_variance(x, lam=0.2, L=3):
    """
    Exponentially weighted moving average control chart
    :param x: input data
    :param lam: λ, the weight given to the most recent rational subgroup mean
    :param L: L, the multiple of the rational subgroup standard deviation that establishes the control limits. L is typically set at 3 to match other control charts, but it may be necessary to reduce L slightly for small values of λ
    :return:
    """
    n = len(x)
    mean = np.mean(x)
    sigma = math.sqrt(np.var(x))
    s = math.sqrt(lam / (2 - lam))
    ucl = np.ones(n) * (mean + L * s * sigma)
    lcl = np.ones(n) * (mean - L * s * sigma)

    return ucl, lcl


def ewma_adaptive_variance(x, lam=0.2, L=3, l=100):
    """
    Exponentially weighted moving average adaptive control chart
    :param x: input data
    :param lam: λ, the weight given to the most recent rational subgroup mean
    :param L: L, the multiple of the rational subgroup standard deviation that establishes the control limits. L is typically set at 3 to match other control charts, but it may be necessary to reduce L slightly for small values of λ
    :return:
    """
    n = len(x)
    ucl = np.zeros(n)
    lcl = np.zeros(n)

    i = 0
    s = math.sqrt(lam / (2 - lam))
    for j in range (l, n+l, l):
        mean = np.mean(x[i:j])
        sigma = math.sqrt(np.var(x[i:j]))
        ucl[i:j] = np.ones(l) * (mean + L * s * sigma)
        lcl[i:j] = np.ones(l) * (mean - L * s * sigma)
        i = j


    return ucl, lcl


def ewmap(x, span=19):
    """
    Exponentially weighted moving average
    :param x: input data
    :param span: center of mass (λ) is calculated as lamda λ = 2/(span + 1), the weight given to the most recent rational subgroup mean
    :return: observations z_i
    """
    import pandas

    return pandas.ewma(x, span=span)


def des(x, alpha=0.1, beta=0.15):
    """
    Double exponential smoothing
    :param x:
    :param alpha: α
    :param beta: β
    :return:
    """
    n = len(x)
    s = np.zeros(n)
    b = np.zeros(n)

    # first step al
    s[0] = x[0]
    b[0] = x[1] - x[0]
    b[0] = 0

    for i in range(1, n):
        s[i] = alpha * x[i] + (1 - alpha) * (s[i - 1] + b[i - 1])
        b[i] = beta * (s[i] - s[i - 1]) + (1 - beta) * b[i - 1]

    return s


def _combine(*args):
    names = []
    for arg in args:
        names.append(arg.func_name)

    def combined(x):
        y = x[:]
        for f in args:
            y = f(y)
        return y

    combined.func_name = '_'.join(names)
    return combined


__all__ = [
    # sma,
    # maww,
    # ewmap,
    ewma_variance,
    ewma_adaptive_variance,
    # des,
    _combine (ewmap, des, maww)
]