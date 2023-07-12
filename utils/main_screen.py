from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5 import Qt
import traceback
from utils.plot import Plot


class MainScreen(QDialog):
    def __init__(self):
        super(MainScreen, self).__init__()
        loadUi("interfaz.ui", self)

    def load_gui_data(self, devices_list):
        # adding list of items to combo box
        self.output_data_index = 0
        self.comboBox.addItems(devices_list)
        # setting current item
        self.started = False
        self.start_button.clicked.connect(self.start)
        self.pause_button.clicked.connect(self.pause)
        self.pixmap = QPixmap('background.jpg')
        self.label = QLabel(self)
        self.label.setPixmap(self.pixmap)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.lower()
        self.setWindowTitle('Reflection Measurment')
        self.f_min.setToolTip('Minimun frequency 100Hz')
        self.f_max.setToolTip('Maximum frequency 1000Hz')
        self.radio_butt_abs.setToolTip('Select if want to plot absorption')
        self.radio_butt_ref.setToolTip('Select if want to plot reflection')
        self.radio_butt_ref.setChecked(True)
        self.start_button.setToolTip('Click to start measure')
        self.pause_button.setToolTip('Click to stop measure')

    def start(self):
        try:
            index = 0
            mic = self.comboBox.currentIndex()
            f_max = int(self.fMax.text())
            f_min = int(self.fMin.text())
            if f_min < 100 or f_min >= f_max or f_min > 1000:
                f_min = 100
            if f_max > 1000 or f_max <= f_min or f_max < 100:
                f_max = 1000
            if self.rBAbsor.isChecked():
                index = 1
            if self.rBReflex.isChecked():
                index = 0
            # Limites plot
            if not self.started:
                self.started = True
                plot = Plot()
                plot.plot(f_min, f_max, index, mic, self.output_data_index)
        except Exception:
            print(traceback.format_exc())
            return None

    def pause(self):
        if self.started:
            self.started = 0
