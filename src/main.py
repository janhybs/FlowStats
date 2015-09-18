# encoding: utf-8
# author:   Jan Hybs
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
import utils.vector
from utils.timer import Timer

timer = Timer()

# uniform distribution: (b - a) * random() + a; sigma = b - a; mu = a
elem_size = 100

spike_prob = 0.2
spike_mu = -25
spike_sigma = 100

mu = -10
sigma = 20

x = np.ones(elem_size) * mu
noise = sigma * np.random.random(elem_size)
spikes = np.array([np.random.random() * spike_sigma + spike_mu if np.random.random() < spike_prob else 0 for i in
                   range(0, elem_size)])

y = x + noise + spikes
t = np.range(elem_size) + 1000

plt.stem(t, y)
plt.ylabel('f(x)')
plt.xlabel('x')
plt.grid(True)
plt.title(r'Histogram of IQ$\,\sigma_i=15$')
plt.show()