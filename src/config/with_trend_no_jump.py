#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

from config import *
import numpy as np

# data with simple linear trend
# data with white/Gaussian noise (constant power spectral density)
# data with impulsive spiky noise
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