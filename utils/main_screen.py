from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from utils.plot import Plot
from utils.constants import CHANNELS, RATE, CHUNK
from utils.helpers import PlotOptions


class MainScreen(QDialog):
    def __init__(self):
        super(MainScreen, self).__init__()
        loadUi("gui.ui", self)
        self._output_data_index = 0
        self._started = False
        self._pixmap = QPixmap('background.jpg')
        self._label = QLabel(self)
        self._plot = Plot()

    def load_gui_data(self, devices_list: list = None):
        """
        Function that receives input/output devices list and loads GUI data.
        Devices list is used to populate a combo box/dropdown.
        :param devices_list: list of devices
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
        from utils.stream import Stream
        mic = self.comboBox.currentIndex()
        # Defining max limits
        f_max = 1000 if self.f_max.text() not in range(100, 1001) else int(self.f_max.text())
        f_min = 100 if self.f_min.text() not in range(100, f_max) else int(self.f_min.text())

        index = PlotOptions(self.radio_butt_abs.isChecked()).value

        # Plot limits
        if not self._plot.started:
            self._plot.started(True)

            stream = Stream(CHANNELS, RATE, CHUNK, mic)
            self._plot(f_min, f_max).plot(self.output_data_index, index, stream, self.export_cb.isChecked())

    def _on_click_pause(self):
        if self._plot.started:
            self._plot.started(False)
