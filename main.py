from utils.helpers import get_input_devices
from PyQt5.QtWidgets import QApplication, QStackedWidget
from utils.main_screen import MainScreen
import sys
try:
    from PyQt5 import sip
except ImportError:
    import sip


if __name__ == '__main__':
    devices_list = get_input_devices()

    # Defining application
    app = QApplication(sys.argv)

    # Instantiate and build main screen
    main_screen = MainScreen()
    main_screen.load_gui_data(devices_list)

    widget = QStackedWidget()
    widget.addWidget(main_screen)
    widget.setFixedWidth(800)
    widget.setFixedHeight(500)
    widget.show()
    try:
        sys.exit(app.exec())
    except SystemExit as e:
        print(e)
