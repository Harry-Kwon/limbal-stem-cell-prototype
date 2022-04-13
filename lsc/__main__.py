import sys
from typing import List
from PySide2.QtWidgets import QApplication
from lsc.views.main_window import MainWindow

class LSCApplication:
    def __init__(self, argv: List[str]):
        self.app = QApplication(sys.argv)
        self.view = MainWindow()

    def start(self):
        self.view.show()
        self.app.exec_()


if __name__ == "__main__":
    app = LSCApplication(sys.argv)
    app.start()