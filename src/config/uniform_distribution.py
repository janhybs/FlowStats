#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

from config import *
import numpy as np

# data without any trend
# data with white/Gaussian noise (constant power spectral density)
# data with impulsive spiky noise
uniform_distribution = [
    {
        'name': 'white-noise',
        'data_size': data_size,
        'function': lambda i: noise_sigma * np.random.rand() + noise_mean
    },
]