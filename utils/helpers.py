import matplotlib.pyplot as plt
import scipy.fft as fft
from tkinter import TclError
import pyaudio
import numpy as np


def get_input_devices():
    device_list = []
    p = pyaudio.PyAudio()
    for i in range(0, 10):
        print(i, p.get_device_info_by_index(i)['name'])
        device_list.append(p.get_device_info_by_index(i)['name'])
    return device_list


def decode(data, CHUNK, channels):
    """
    Convert a byte stream into a 2D numpy array with
    shape (chunk_size, channels)

    Samples are interleaved, so for a stereo stream with left channel
    of [L0, L1, L2, ...] and right channel of [R0, R1, R2, ...], the output
    is ordered as [L0, R0, L1, R1, ...]
    """
    # TODO: handle data type as parameter, convert between pyaudio/numpy types
    result = np.fromstring(data, dtype=np.float32)

    result = np.reshape(result, (CHUNK, channels))
    return result
