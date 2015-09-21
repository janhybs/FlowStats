#!/usr/bin/python
# -*- coding: utf-8 -*-
# author:   Jan Hybs

class Colors(object):
    @staticmethod
    def create(space='normal', size=5):
        if space == 'normal':
            colors = ['k', 'r', 'g', 'b', 'c', 'm', 'y', 'k']
            colors.reverse()

        if space == 'blue':
            colors = [(0, 0, float(x) / size) for x in range(1, size + 1)]

        if space == 'red' or space == 'datafilter':
            colors = [(float(x) / size, 0, 0) for x in range(1, size + 1)]

        if space == 'green':
            colors = [(0, float(x) / size, 0) for x in range(1, size + 1)]

        if space == 'datafilter':
            colors.append('k')

        colors = colors * 10
        return Colors(colors)

    def __init__(self, colors):
        self.colors = list(colors)
        self.backup = list(colors)
        self.previous = None

    def reset(self):
        self.colors = list(self.backup)

    def prev(self):
        return self.previous

    def next(self):
        self.previous = self.colors.pop()
        return self.previous
