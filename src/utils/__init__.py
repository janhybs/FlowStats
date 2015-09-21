#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs


import numpy as np


def np_range(start, stop=None, step=1):
    """
    shortcut for range creation
    :param start:
    :param stop:
    :param step:
    :return:
    """
    return np.array(range(start, stop, step)) if stop is not None else np.array(range(0, start))


np.range = np_range