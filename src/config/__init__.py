#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

import numpy as np
import math

# number of elements
data_size = 1000

# mean value and trend change
mean = 100
trend = 50

# noise standard deviation and mean
noise_sigma = 10
noise_mean = 0

# spike standard deviation, mean and probability of spike occurrence
spike_sigma = 50
spike_mean = 0
spike_prob = 0.95


class Config(list):
    def __init__(self, name, iterable):
        super(Config, self).__init__(iterable)
        self.name = name


# data without any trend
# data with white/Gaussian noise (constant power spectral density)
# data with impulsive spiky noise
data_simple = Config('data_simple', [
    {
        'name': 'data',
        'data_size': data_size,
        'function': lambda i: mean
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
        'function': lambda i: np.random.normal(spike_mean, spike_sigma) if np.random.random() >= spike_prob else 0.0
    },
])


# data with simple linear trend
# data with white/Gaussian noise (constant power spectral density)
# data with impulsive spiky noise
data_trend = Config('data_trend', [
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
])


# data with simple linear trend
# data with white/Gaussian noise (constant power spectral density)
# data with impulsive spiky noise
data_trend_jump = Config('data_trend_jump', [
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
    {
        'name': 'jump',
        'data_size': data_size,
        'function': lambda i: spike_sigma if i > data_size/2 else 0
    },
])


# data with simple linear trend
# data with white/Gaussian noise (constant power spectral density)
# data with impulsive spiky noise
data_reversed_trend = Config('data_reversed_trend', [
    {
        'name': 'data',
        'data_size': data_size,
        'function': lambda i: mean + (float(data_size - i) / data_size) * trend
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
])


# data with sinus-like trend
# data with white/Gaussian noise with increasing variance, sigma from noise_sigma/2 to noise_sigma*5
# data with impulsive spiky noise
data_variation = Config('data_variations', [
    {
        'name': 'data',
        'data_size': data_size,
        'function': lambda i: mean
    },
    {
        'name': 'white-noise',
        'data_size': data_size,
        'function': lambda i: np.random.normal(noise_mean, noise_sigma) * ((float(i) / (data_size)) * 4.5 + 0.5)
    },
])


# data with sinus-like trend
# data with white/Gaussian noise (constant power spectral density)
# data with impulsive spiky noise
data_complex_trend = Config('data_complex_trend', [
    {
        'name': 'data',
        'data_size': data_size,
        'function': lambda i: mean + trend * math.sin(((float(i) / data_size) * math.pi * 2))
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
])


# data without any trend
# data with white/Gaussian noise (constant power spectral density)
# data with impulsive spiky noise
normal_distribution = Config('normal_distribution', [
    {
        'name': 'white-noise',
        'data_size': data_size,
        'function': lambda i: np.random.normal(noise_mean, noise_sigma)
    },
])


# data without any trend
# data with white/Gaussian noise (constant power spectral density)
# data with impulsive spiky noise
uniform_distribution = Config('uniform_distribution', [
    {
        'name': 'white-noise',
        'data_size': data_size,
        'function': lambda i: noise_sigma * np.random.rand() + noise_mean
    },
])