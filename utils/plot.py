import numpy as np
import matplotlib.pyplot as plt
import scipy.fft as fft
import pandas as pd
from utils.helpers import decode
import pyaudio
from utils import constants


class Plot:
    def __init__(self, stream):
        self.stream = p.open(
            format=pyaudio.paFloat32,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            output=False,
            frames_per_buffer=CHUNK,
            input_device_index=mic)

        fig, (r, absr) = plt.subplots(2, figsize=(15, 7))
        line, = r.semilogx(F, np.random.rand(CHUNK), '-', lw=2)
        line2, = absr.semilogx(F, np.random.rand(CHUNK), '-', lw=2)

        r.set_ylim(0, 1.25)
        r.set_xlim(f_min, f_max)
        absr.set_ylim(0, 0.025)
        absr.set_xlim(f_min, f_max)

    def plot(self, f_min, f_max, index, mic, output_data_index):
        plt.show(block=False)
        while self.started:
            # Binary data
            data = self.stream.read(CHUNK)
            result = decode(data, CHUNK, CHANNELS)

            # FFT and Y Data
            try:
                y_fft = fft.fft(result[:, 0])
                y_fft2 = fft.fft(result[:, 1])

                y_fft = fft.fftshift(y_fft / RATE)
                y_fft2 = fft.fftshift(y_fft2 / RATE)

                hi = np.exp(-1j * ko * s)
                hr = np.exp(1j * ko * s)
                h12 = y_fft / y_fft2
                r = ((h12 - hi) / (hr - h12)) * np.exp(2 * 1j * ko * dist)
                absr = (1 - abs(r) ** 2)
                output_data_index += 1

                if index == 0:
                    line.set_ydata(abs(r))
                    line2.set_ydata(abs(y_fft))
                if index == 1:
                    line.set_ydata(absr)
                    line2.set_ydata(abs(y_fft))

                fig.canvas.flush_events()
                fig.canvas.draw()

                # Exporting absorption data to CSV file

                Fround = [round(item, 1) for item in F]
                lowFreq = list(Fround).index(float(f_min))
                highFreq = list(Fround).index(float(f_max))

                absorTmp = {
                    "Frequency": F[lowFreq:highFreq],
                    "Absorption coefficient": absr[lowFreq:highFreq]
                }
                absorData = pd.DataFrame(absorTmp)
                absorData.to_csv(f"absorption{output_data_index}.csv", index=False, sep=";")

                # Exporting reflection data to CSV file
                reflecTmp = {
                    "Frequency": F,
                    "Reflection coefficient": abs(r)
                }
                reflecData = pd.DataFrame(reflecTmp)
                reflecData.to_csv(f"reflection{output_data_index}.csv", index=False, sep=";")

            except Exception:
                print(traceback.format_exc())
                print('Stream stopped')
                break
        plt.close()