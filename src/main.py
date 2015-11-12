#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs
import math

import numpy as np
import collections
import filters as fltrs
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from data import generate_data

from utils.colors import Colors
from utils.subplots import Subplots
from utils.timer import Timer
from config import *


timer = Timer()
colors = Colors(['normal'] * 10)
data = []
filtered = []

filters = [
    # fltrs.ewma,
    fltrs.ewma_adaptive_variance_linear,
    # fltrs.ewma_variance,
    # fltrs.maww,
    # fltrs.des
]

configs = [
    data_trend,
    # data_simple,
    data_complex_trend,
    data_variation,
    # data_reversed_trend,
    data_trend_jump,
]
for config in configs:
    data.append(generate_data(config))

for f in filters:
    index = filters.index(f)
    filtered.append([])
    for x, y in data:
        print "Filtering data using {}".format(f.func_name)
        x_ = f(x)
        y_ = np.range(len(x_)) if type(x_) is not tuple else ([range(len(x_[0]))] * len(x_))
        filtered[index].append((x_, y_))

dim = Subplots.get_dimensions(len(data))
figure, subplots = plt.subplots(*dim, sharex=True, sharey=True)
plots = Subplots(subplots)
plots.grid(True)

colors.reset()
for i in range(len(data)):
    c = Colors.create(colors.next(), len(filters))
    plots[i].plot(data[i][1], data[i][0], '.-', c=c.next(), lw=0.1)
    legends = [mpatches.Patch(color=c.prev(), label=configs[i].name)]

    for f in filters:
        j = filters.index(f)
        filter_data_x = filtered[j][i][0]
        filter_data_y = filtered[j][i][1]
        if type(filter_data_x) is tuple:
            cc = c.next()
            for k in range(len(filter_data_x)):
                plots[i].plot(filter_data_y[k], filter_data_x[k], c=cc)
        else:
            plots[i].plot(filter_data_y, filter_data_x, '.-', c=c.next(), lw=0.2)
        legends.append(mpatches.Patch(color=c.prev(), label=f.func_name))

    plots[i].legend(handles=legends, loc=0)

plt.show()
