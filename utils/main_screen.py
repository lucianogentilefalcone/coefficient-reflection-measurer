from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from utils.plot import Plot
from utils.constants import CHANNELS, RATE, CHUNK
from utils.helpers import PlotOptions


class MainScreen(QDialog):
    def __init__(self, plotter: Plot = None):
        super(MainScreen, self).__init__()
        loadUi("gui.ui", self)
        self._output_data_index = 0
        self._started = False
        self._pixmap = QPixmap('background.jpg')
        self._label = QLabel(self)
        self._plot = plotter or Plot()

    def load_gui_data(self, devices_list: list = None):
        """
        Function that receives input/output devices list and loads GUI data.
        Devices list is used to populate a combo box/dropdown.
        :param devices_list: list of devices
        :param plotter
        """
        # adding list of items to combo box
        if devices_list is None:
            devices_list = []
        self.comboBox.addItems(devices_list)
        # setting current item
        self.start_button.clicked.connect(self._on_click_start)
        self.pause_button.clicked.connect(self._on_click_pause)
        self._label.setPixmap(self._pixmap)
        self._label.setAlignment(Qt.AlignCenter)
        self._label.lower()
        self.setWindowTitle('Reflection Measurment')
        self.f_min.setToolTip('Minimun frequency 100Hz')
        self.f_max.setToolTip('Maximum frequency 1000Hz')
        self.radio_butt_abs.setToolTip('Select if want to plot absorption')
        self.radio_butt_ref.setToolTip('Select if want to plot reflection')
        self.radio_butt_ref.setChecked(True)
        self.start_button.setToolTip('Click to start measure')
        self.pause_button.setToolTip('Click to stop measure')

    def _on_click_start(self):
        from utils.stream import AudioStream
        mic = self.comboBox.currentIndex()

        index = PlotOptions(self.radio_butt_abs.isChecked()).value

        # Plot limits
        if not self._plot.started:
            self._plot.started = True
            audio_stream = AudioStream(CHANNELS, RATE, CHUNK, mic).stream
            self._plot.set_axis_limits(f_min=int(self.f_min.text()), f_max=int(self.f_max.text()))
            self._plot.plot(index, audio_stream, self.export_cb.isChecked())

    def _on_click_pause(self):
        if self._plot.started:
            self._plot.started = False
