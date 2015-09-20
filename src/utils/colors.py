#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

class Colors(object):
    @staticmethod
    def create(space='normal', size=5):
        if space == 'normal':
            colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
            colors.reverse()

        if space == 'blue':
            colors = [(0, 0, float(x) / size) for x in range(1, size+1)]

        if space == 'red':
            colors = [(float(x) / size, 0, 0) for x in range(1, size+1)]

        if space == 'green':
            colors = [(0, float(x) / size, 0) for x in range(1, size+1)]

        colors = colors * 10
        return Colors(colors)

    def __init__(self, colors):
        self.colors = list(colors)
        self.backup = list(colors)

    def reset(self):
        self.colors = list(self.backup)

    def next(self):
        return self.colors.pop()
