#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs
import base64
from tempfile import NamedTemporaryFile

import numpy as np
import matplotlib.pyplot as plt


class DataConfig(object):
    def __init__(self, size, generator, start=0):
        self.size = size
        self.generator = generator
        self.start = start


def constant_generator(mu=0.0, sigma=1.0):
    def generator(i):
        return np.random.normal(mu, sigma)
    return generator


def spread_generator(mu=0.0, sigma=1.0, sigma_step=1.0):
    def generator(i):
        return np.random.normal(mu, sigma_step*i + sigma)

    return generator


def exp_spread_generator(mu=0.0, sigma=1.0, power=2):
    def generator(i):
        return np.random.normal(mu, sigma*(i**power) + 0.0001)

    return generator


def linear_generator(scale=1.0, mu=0.0, sigma=1.0):
    def generator(i):
        return i * scale + np.random.normal(mu, sigma)
    return generator


def exponential_generator(scale=1.0, power=2, mu=0.0, sigma=1.0):
    def generator(i):
        return (i ** power) * scale + np.random.normal(mu, sigma)
    return generator


def generate(configs):
    """
    :rtype: numpy.core.multiarray.ndarray
    :type configs: list[DataConfig]
    """
    data = []
    for config in configs:
        config_data = [config.generator(i) for i in range(config.start, config.start + config.size)]
        data.extend(config_data)

    return np.array(range(len(data)), dtype=np.float32), np.array(data, dtype=np.float32)


def plot(data, color, method='scatter', **kwargs):
    getattr(plt, method)(*data, c=color, **kwargs)


# size  = 100
# mu    = 0
# sigma = 1
# lam   = 0.2
# L     = 3
#
# data = generate([
#     DataConfig(int(size / 2), constant_generator(mu, sigma)),
#     DataConfig(size - int(size / 2), spread_generator(mu, sigma, sigma / 5))
# ])
# ucl, lcl = filters.ewma_adaptive_variance_linear(*data, lam=lam, L=L, l=10)

# scatter_settings = dict(edgecolors='none')
# data = generate(
#     [
#         DataConfig(300, constant_generator(sigma=0.5)),
#         DataConfig(300, constant_generator(sigma=2.0)),
#         DataConfig(300, exponential_generator(scale=0.0001)),
#         DataConfig(300, linear_generator(scale=0.01), start=int(300*300*0.01))
#     ]
# )
#
# # generate data
# sma_data = filters.sma_filter(*data)
# maww_data = filters.maww_filter(*data)
# ewma_data = filters.ewma_filter(*data)
# des_data = filters.des_filter(*data)
#
# # plot data and filtered data
# plot(data,      'blue',     'scatter', **scatter_settings)
# plot(sma_data,  'red',      'plot')
# plot(maww_data, 'green',    'plot')
# plot(ewma_data, 'black',    'plot')
# plot(des_data,  'brown',    'plot')
#
# combining filters
# des_ewma = filters.combine_filter(filters.des_filter, filters.ewma_filter)
# plot(des_ewma(*data), 'pink', 'scatter')
#
# # plot control chart
# ucl, lcl = filters.ewma_variance(*data)
# plot(ucl, 'purple', 'plot')
# plot(lcl, 'purple', 'plot')
#
# # dynamic controls
# ducl, dlcl = filters.ewma_adaptive_variance_linear(*data)
# plot(ducl, 'orange', 'plot')
# plot(dlcl, 'orange', 'plot')
# #
# plt.show()
#


# data = generate([
#     DataConfig(100, spread_generator())
# ])
#
# plt.scatter(*data)
# plt.show()
#
# from tempfile import NamedTemporaryFile
#
# VIDEO_TAG = """<video controls>
#  <source src="data:video/x-m4v;base64,{0}" type="video/mp4">
#  Your browser does not support the video tag.
# </video>"""
#
# def anim_to_html(anim):
#     if not hasattr(anim, '_encoded_video'):
#         with NamedTemporaryFile(suffix='.mp4') as f:
#             anim.save(f.name, fps=20, extra_args=['-vcodec', 'libx264'])
#             video = open(f.name, "rb").read()
#         anim._encoded_video = video.encode("base64")
#
#     return VIDEO_TAG.format(anim._encoded_video)
#
#
# from IPython.display import HTML
#
# def display_animation(anim):
#     plt.close(anim._fig)
#     return HTML(anim_to_html(anim))
# import matplotlib.animation as animation
#
#
# size = 100
#
# def update_line(num, data, line):
#     line.set_data(data[...,:num])
#     return line,
#
# fig1 = plt.figure()
#
# data = np.random.rand(2, size)
# l, = plt.plot([], [], 'r-')
# plt.xlim(0, 1)
# plt.ylim(0, 1)
# plt.xlabel('x')
# plt.title('test')
# anim = animation.FuncAnimation(fig1, update_line, 25, fargs=(data, l), interval=50, blit=True)
# anim.to
#
#
# print (anim.to_html5_video())
# VIDEO_TAG = """<video controls>
#  <source src="data:video/x-webm;base64,{0}" type="video/webm">
#  Your browser does not support the video tag.
# </video>"""
#
#
# def anim_to_html(anim):
#     if not hasattr(anim, '_encoded_video'):
#         with NamedTemporaryFile(suffix='.webm') as f:
#             anim.save(f.name, fps=6, extra_args=['-vcodec', 'libvpx'])
#             video = open(f.name, "rb").read()
#         anim._encoded_video = base64.b64encode(video)
#
#     return VIDEO_TAG.format(anim._encoded_video.decode('ascii'))
#
#
#
# def display_animation(anim):
#     from IPython.display import HTML
#     plt.close(anim._fig)
#     return HTML(anim_to_html(anim))
#
# anim_to_html(anim)

# s = plt.scatter(1, 2)
