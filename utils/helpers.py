import pyaudio
import numpy as np
import scipy.fft as fft
from utils.constants import RATE, K0, S, DIST
from enum import Enum


class PlotOptions(Enum):
    REFLECTION_COEFFICIENT = 0
    ABSORPTION_COEFFICIENT = 1


def process_raw_data(input_data: list[float]) -> tuple[float, float]:
    y_fft = fft.fft(input_data[:, 0])
    y_fft2 = fft.fft(input_data[:, 1])

    y_fft = fft.fftshift(y_fft / RATE)
    y_fft2 = fft.fftshift(y_fft2 / RATE)

    hi = np.exp(-1j * K0 * S)
    hr = np.exp(1j * K0 * S)
    h12 = y_fft / y_fft2
    reflection_coefficient = ((h12 - hi) / (hr - h12)) * np.exp(2 * 1j * K0 * DIST)
    return reflection_coefficient, y_fft


def get_input_devices():
    device_list = []
    p = pyaudio.PyAudio()
    for i in range(0, 10):
        print(i, p.get_device_info_by_index(i)['name'])
        device_list.append(p.get_device_info_by_index(i)['name'])
    return device_list


def decode(data, chunk, channels):
    """
    Convert a byte stream into a 2D numpy array with
    shape (chunk_size, channels)

    Samples are interleaved, so for a stereo stream with left channel
    of [L0, L1, L2, ...] and right channel of [R0, R1, R2, ...], the output
    is ordered as [L0, R0, L1, R1, ...]
    """
    # TODO: handle data type as parameter, convert between pyaudio/numpy types
    result = np.fromstring(data, dtype=np.float32)

    result = np.reshape(result, (chunk, channels))
    return result
