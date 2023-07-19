import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from utils.helpers import decode, process_raw_data, PlotOptions
from utils.constants import CHANNELS, CHUNK, F, MIN_FREQUENCY, MAX_FREQUENCY


class PlotException(BaseException):
    pass


class Plot:
    def __init__(self):
        self._plot_started = False
        self.reflection_coefficient = None
        self.y_axis_fft = None
        self.absorption = None
        self.output_data_index = 0
        self.fig, (self.plot_r, self.plot_power) = plt.subplots(2, figsize=(15, 7))
        self.line, = self.plot_r.semilogx(F, np.random.rand(CHUNK), '-', lw=2)
        self.line2, = self.plot_power.semilogx(F, np.random.rand(CHUNK), '-', lw=2)
        self.f_min = 100
        self.f_max = 1000
        pass

    @property
    def started(self):
        return self._plot_started

    @started.setter
    def started(self, status: bool = None):
        if not isinstance(status, bool):
            raise PlotException(f"Wrong datatype was given. Expected bool got {type(status)}")
        self._plot_started = status

    def _show_plot(self, plot_selection):
        plot_data = self.reflection_coefficient if plot_selection == PlotOptions.REFLECTION_COEFFICIENT.value \
            else (1 - abs(self.reflection_coefficient) ** 2)
        self.line.set_ydata(abs(plot_data))
        self.line2.set_ydata(abs(self.y_axis_fft))
        self.fig.canvas.flush_events()
        self.fig.canvas.draw()

    def _export_data(self, output_data_index, plot_selection):
        # Exporting plot data to CSV file
        f_round = [round(item, 1) for item in F]
        low_freq = list(f_round).index(float(self.f_min))
        high_freq = list(f_round).index(float(self.f_max))

        export_data = self.reflection_coefficient if plot_selection == PlotOptions.REFLECTION_COEFFICIENT.value \
            else (1 - abs(self.reflection_coefficient) ** 2)

        output_data = {
            "Frequency": F[low_freq:high_freq],
            PlotOptions(plot_selection).name.lower(): abs(export_data[low_freq:high_freq])
        }

        output_data_pd = pd.DataFrame(output_data)
        file_name = f'{PlotOptions(plot_selection).name.lower().lower()}_{output_data_index}.csv'
        output_data_pd.to_csv(file_name, index=False, sep=";")

    def set_axis_limits(self,
                        f_min: int = None,
                        f_max: int = None,
                        coef_lower: float = 0,
                        coef_higher: float = 1.25,
                        power_lower: float = 0,
                        power_higher: float = 0.025
                        ):
        # Defining max limits
        self.f_min = f_min if f_min in range(MIN_FREQUENCY, MAX_FREQUENCY) else self.f_min
        self.f_max = f_max if f_max in range(self.f_min, MAX_FREQUENCY) else self.f_max
        self.plot_r.set_ylim(coef_lower, coef_higher)
        self.plot_r.set_xlim(self.f_min, self.f_max)
        self.plot_power.set_ylim(power_lower, power_higher)
        self.plot_power.set_xlim(self.f_min, self.f_max)

    def plot(self, plot_selection, stream, export_data):
        plt.show(block=False)
        while self._plot_started:
            # Binary data
            data = stream.read(CHUNK)
            decoded_data = decode(data, CHUNK, CHANNELS)

            self.output_data_index += 1

            self.reflection_coefficient, self.y_axis_fft = process_raw_data(decoded_data)
            self._show_plot(plot_selection)
            if export_data:
                self._export_data(self.output_data_index, plot_selection)
        plt.close()
        stream.close()
