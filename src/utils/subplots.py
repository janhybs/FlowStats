#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs
import math

import numpy as np


class Subplots(object):
    def __init__(self, subplots):
        self.subplots = None
        self.dim_y = None
        self.dim_x = None

        if type(subplots) is not np.ndarray:
            self.subplots = np.array([subplots])
        else:
            self.subplots = subplots.copy()

        self.dim_y = len(self.subplots)
        for i in range(self.dim_y):
            if type(self.subplots[i]) is not np.ndarray:
                self.subplots[i] = np.array([self.subplots[i]])
            else:
                self.subplots[i] = self.subplots[i].copy()

            self.dim_x = len(self.subplots[i])

        self.size = self.dim_y * self.dim_x

    def grid(self, value):
        for i in range(self.size):
            self[i].grid(value)

    def get(self, x, y):
        return self.subplots[x][y]

    def __getitem__(self, n):
        x = n / self.dim_x
        y = n % self.dim_x
        return self.subplots[x][y]

    @staticmethod
    def get_dimensions(n):
        if n < 2:
            return 1, 1

        if n < 3:
            return 2, 1

        if n < 5:
            return 2, 2

        if n < 7:
            return 2, 3

        return 3, int(math.ceil(n / 3.0))