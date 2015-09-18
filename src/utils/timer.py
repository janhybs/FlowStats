# encoding: utf-8
# author:   Jan Hybs
import time


class Timer(object):
    def __init__(self):
        self.times = { }
        self.names = { }
        self.prints = {}
        self.level = 0

    def __enter__(self):
        self.times[self.level] = time.time()
        self.level += 1
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.level -= 1
        self.times[self.level] = time.time() - self.times[self.level]

        if self.prints[self.level]:
            print "{:s} {:s}".format(Timer.format_name(self.names[self.level], self.level),
                                     Timer.format_time(self.times[self.level]))
        return self

    def time(self):
        return self.times[self.level]

    def measured(self, name, print_name=True):
        self.names[self.level] = name
        self.prints[self.level] = print_name
        return self

    @staticmethod
    def format_name(name, level):
        return "{:80s}".format(level * '  ' + name)

    @staticmethod
    def format_time(value):
        n = "{:3.3f} ms".format(value * 1000)
        return "{0: >15}".format(n)


    @staticmethod
    def measure(method):
        def timed(*args, **kw):
            ts = time.time()
            result = method(*args, **kw)
            te = time.time()
            # print '%r (%r, %r) %2.2f sec' % (method.__name__, args, kw, te-ts)
            print '{:80s} {:s}'.format(method.__name__, Timer.format_time(te - ts))
            return result

        return timed