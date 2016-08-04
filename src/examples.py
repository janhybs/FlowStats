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
    yii = np.argsort(yi)  # inverse

    # xs = np.array([x[i] for i in xi])
    # ys = np.array([y[i] for i in xi])
    # ysy = np.array([y[i] for i in yi])

    xr = np.range(n) + 1
    yr = np.array([yii[i] for i in xi]) + 1
    dr = (xr - yr) * (xr - yr)
    ds = np.sum(dr)

    return 1 - (6.0 * ds) / (n * (n * n - 1.0))


def mean(x):
    """
    x-bar = mean and expected value are used synonymously to refer to one measure of the central
        tendency either of a probability distribution or of the random variable
        characterized by that distribution
    :param x:
    :return:
    """
    n = len(x)
    return np.sum(x) / n


def variance(x):
    """
    s^2 = measures how far a set of numbers is spread out
    :param x:
    :return:
    """
    n = len(x)
    xbar = mean(x)
    return (np.sum(x * x) - n * (xbar * xbar)) / (n - 1)


def standard_deviation(x):
    """
    sqrt(s^2) = s
    :param x:
    :return:
    """
    return math.sqrt(variance(x))


def median(x):
    """
    median is the number separating the higher half of a data sample, a population, or a probability distribution, from the lower half
    :param x:
    :return:
    """
    n = len(x)
    sx = np.sort(x)
    if n % 2 == 0:
        return (sx[(n - 1) / 2] + sx[(n) / 2]) / 2
    return sx[n / 2]


def quantile(x, percent=0.25):
    n = len(x)
    sx = np.sort(x)
    if n * percent == int(n * percent):
        return (sx[(n - 1) * percent] + sx[(n) * percent]) / 2
    return sx[n * percent]


def modus(x):
    occurrences = { }
    for value in x:
        if occurrences.get(str(value), None) is None:
            occurrences[str(value)] = 0
        occurrences[str(value)] += 1

    max_occurrence = max(occurrences.values())
    max_list = list()
    for value in occurrences.keys():
        if occurrences[value] == max_occurrence:
            max_list.append(value)
    return float(max_list[0]) if len(max_list) == 1 else None


def histogram(x, bins=10):
    # return np.histogram(x, bins)
    min_value = min(x)
    max_value = max(x)
    delta = float(max_value - min_value)
    step = delta / bins

    bins_list = [-float("inf")] + [min_value + step * i for i in range(1, bins + 1)]
    hist = [0] * (len(bins_list) - 1)

    for value in x:
        for i in range(0, len(bins_list) - 1):
            if bins_list[i] < value <= bins_list[i + 1]:
                hist[i] += 1
                break

    return hist, bins_list


def regression_line(x, y):
    # \hat{\beta} = \sum {y_i(x - \bar{x}}) / \sum{(x_i - \bar{x})^2}
    # \hat{\beta} = \frac{\bar{xy} - \bar{x}\bar{y}} { \bar{x^2} - \bar{x}^2 }
    # \hat{\alpha} = \bar{y} - \hat{\beta}\bar{x}
    beta = np.sum(y * (x - np.mean(x))) / np.sum((x - np.mean(x)) * (x - np.mean(x)))
    alpha = np.mean(y) - beta * np.mean(x)
    return beta, alpha




# x = np.array([0, 1, 2, 3])
# # x = np.array([30, 61, 42, 19, 47, 52, 35, 27.])
# y = np.array([-2, 0.2, 0.9, 2.1])
# # y = np.array([1.6, 2.8, 2.2, 1.4, 2.7, 2.5, 2.6, 1.9])
#
#
# # print regression_line(x, y)
#
# X = np.vstack([x * 0 + 1, x, x * x]).T
# alpha = np.zeros(len(x))
# print np.dot(np.dot(np.linalg.inv(np.dot(X.T, X)), X.T), y)
#
# print alpha
#
# exit(0)
# beta, alpha = regression_line(x, y)
# plt.scatter(x, y)
# plt.plot(x, x * beta + alpha, 'r', label='Fitted line')
# beta = 0.0148
# plt.plot(x, x * beta + alpha)
# beta = 0.0502
# plt.plot(x, x * beta + alpha)
# plt.legend()
# plt.show()
#
# print pearsonr(x, y)
#
# exit(0)
#
# x = np.array([106., 86, 100, 101, 99, 103, 97, 113, 112, 110])
# y = np.array([7, 0, 27, 50, 28, 29, 20, 12, 6, 17])
#
# x = np.array([12, 27, 20, 19, 20, 15, 23, 14, 26, 22, 19, 21, 20, 17, 32, 23.])
#
# print histogram(x)
# #
# print scipy.stats.stats.spearmanr(x, y)
# print spearmanr (x, y)
# print pearsonr(x, y)
#
# plt.scatter(x, y)
# plt.show()