#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs
import math

import numpy as np
import utils
import scipy
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


y = np.linspace(0, 99, 100) + 5 + np.random.random(100)*100
x = np.range(100)


# correlation
x_mean = np.mean(x)
y_mean = np.mean(y)
x_ = x - x_mean
y_ = y - y_mean
#  =

xy = np.sum (x_ * y_)
xx = np.sum (x_ * x_)
yy = np.sum (y_ * y_)

# Pearson correlation coefficient.
correlation = xy / math.sqrt(xx * yy)

print scipy



plt.plot(x, y)
plt.plot(x_, y_)
plt.show()