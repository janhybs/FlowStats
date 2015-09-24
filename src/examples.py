#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs
import math

import numpy as np
import utils
import scipy.stats
import matplotlib.pyplot as plt
#
#
# x = np.array([0.0, 1.0, 2.0, 3.0,  4.0,  5.0])
# y = np.array([0.0, 0.8, 0.9, 0.1, -0.8, -1.0])
# z = np.polyfit(x, y, 3)
# p = np.poly1d(z)
# print p
#
# p10 = np.poly1d(np.polyfit(x, y, 10))
#
#
# xp = np.linspace(-2, 6, 100)
# plt.plot(x, y, '.', label="Original Data")
# plt.plot(xp, p(xp), '-', label="3rd order polynomal fit")
# plt.plot(xp, p10(xp), '--', label="10th order polynomal fit")
# plt.ylim(-2,2)
# plt.legend()
# plt.show()
#
#
# n = 1000
# x = np.range(n) + np.random.random(n)*1000
# y = np.range(n)
# x = -np.array([0, 1, 2, 3])
# y = np.array([-1, 0.2, 0.9, 2.1])
#
#
# A = np.vstack([x, np.ones(len(x))]).T
# m, c = np.linalg.lstsq(A, y)[0]
#
# print "Increasing" if m > 0 else "Decreasing"
# print np.poly1d((m, c))
#
# plt.plot(x, y, 'o', label='Original data', markersize=10)
# plt.plot(x, m*x + c, 'r', label='Fitted line')
# plt.legend()
# plt.show()


y = np.linspace(0, 99, 100) + 5 + np.random.random(100) * 100
x = np.range(100)


def pearsonr(x, y):
    """
    Pearson product-moment correlation coefficient, measure of the linear correlation between
        two variables X and Y, giving a value between +1 and −1 inclusive, where 1 is total
        positive correlation, 0 is no correlation, and −1 is total negative correlation.
    :param x:
    :param y:
    :return:
    """
    xm, ym = np.mean(x), np.mean(y)

    xn, yn = x - xm, y - ym
    return np.sum(xn * yn) / math.sqrt(np.sum(xn * xn) * np.sum(yn * yn))


def spearmanr(x, y):
    """
    Spearman's rank correlation coefficient, nonparametric measure of statistical dependence between
        two variables. It assesses how well the relationship between two variables can be
        described using a monotonic function. If there are no repeated data values,
        a perfect Spearman correlation of +1 or −1 occurs when each of the variables
        is a perfect monotone function of the other.
    :param x:
    :param y:
    :return:
    """
    n = len(x)
    xi = np.argsort(x)
    yi = np.argsort(y)
    yii = np.argsort(yi)

    # xs = np.array([x[i] for i in xi])
    # ys = np.array([y[i] for i in xi])
    # ysy = np.array([y[i] for i in yi])

    xr = np.range(n) + 1
    yr = np.array([yii[i] for i in xi]) + 1
    dr = (xr - yr) * (xr - yr)
    ds = np.sum(dr)

    return 1 - (6.0 * ds) / (n * (n * n - 1.0))


x = np.array([106, 86, 100, 101, 99, 103, 97, 113, 112, 110])
y = np.array([  7,  0,  27,  50, 28,  29, 20,  12,   6,  17])


print scipy.stats.stats.spearmanr(x, y)
print spearmanr (x, y)
print pearsonr(x, y)

plt.scatter(x, y)
plt.show()