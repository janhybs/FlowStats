#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

from config import *
import numpy as np

# data without any trend
# data with white/Gaussian noise (constant power spectral density)
# data with impulsive spiky noise
normal_distribution = [
    {
        'name': 'white-noise',
        'data_size': data_size,
        'function': lambda i: np.random.normal(noise_mean, noise_sigma)
    },
]