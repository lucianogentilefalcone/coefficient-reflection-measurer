# constants.py
import numpy as np

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
T = 1  # Period of sampling in seconds
CHANNELS = 2  # Number of channels
RATE = 44100  # Sampling rate
CHUNK = T * RATE  # Amount of samples
F = np.arange(-RATE / 2, RATE / 2, RATE / CHUNK)  # Frequency to plot
FREQ = np.arange(0, RATE, -RATE / CHUNK)  # Frequency to plot
C = 328  # Speed of sound
PI = np.pi  # Pi
S = 0.135  # Distance between the
DIST = 0.385  #
K0 = 2 * PI * F / C
MAX_FREQUENCY = 1000
MIN_FREQUENCY = 100
