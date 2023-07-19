import sys
from utils.helpers import get_input_devices
from PyQt5.QtWidgets import QApplication, QStackedWidget
from utils.main_screen import MainScreen
from utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT


if __name__ == '__main__':
    devices_list = get_input_devices()

    # Defining application
    app = QApplication(sys.argv)

    # Instantiate and build main screen
    main_screen = MainScreen()
    main_screen.load_gui_data(devices_list)

    widget = QStackedWidget()
    widget.addWidget(main_screen)
    widget.setFixedWidth(WINDOW_WIDTH)
    widget.setFixedHeight(WINDOW_HEIGHT)
    widget.show()
    try:
        sys.exit(app.exec())
    except SystemExit as e:
        print(e)
