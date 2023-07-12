# constants.py
import numpy as np


CHANNELS = 2
RATE = 44100
CHUNK = 10 * RATE
F = np.arange(-RATE / 2, RATE / 2, RATE / CHUNK)
FREQ = np.arange(0, RATE, -RATE / CHUNK)
C = 328
PI = np.pi
S = 0.135
DIST = 0.385
K0 = 2 * PI * F / C
