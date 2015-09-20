#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

from config import *
import numpy as np
import math

# data with sinus-like trend
# data with white/Gaussian noise with increasing variance, sigma from noise_sigma/2 to noise_sigma*2
# data with impulsive spiky noise
no_trend_no_jump_with_variation = [
    {
        'name': 'data',
        'data_size': data_size,
        'function': lambda i: mean
    },
    {
        'name': 'white-noise',
        'data_size': data_size,
        'function': lambda i: np.random.normal(noise_mean, noise_sigma)* ((float(i)/(data_size))*1.5 + 0.5)
    },
]