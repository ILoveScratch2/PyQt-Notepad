from ui import Ui_window
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal


class MainWindow(QtWidgets.QMainWindow, Ui_window):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.width = None
        self.height = None
        self.setupUi(self)

    @property
    def window_title(self):
        return "Notepad"

    @window_title.setter
    def window_title(self, value):
        self.setWindowTitle(value)

    resized = pyqtSignal()

    def resizeEvent(self, event):
        self.width = event.size().width()
        self.height = event.size().height()
        self.resized.emit()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
