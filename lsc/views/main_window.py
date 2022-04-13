from PySide2.QtWidgets import QMainWindow, QWidget, QGridLayout
from PySide2.QtCore import Qt
from .menubar import MenuBar
from .image_viewer import ImageViewer
from .tools_area import ToolsArea

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 800, 600)
        self.menubar = MenuBar()
        self.setMenuBar(self.menubar)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        centralLayout: QGridLayout = QGridLayout(centralWidget)
        centralLayout.setColumnStretch(0, 1)
        centralLayout.setColumnStretch(1, 0)
        centralWidget.setLayout(centralLayout)

        self.image_viewer = ImageViewer()
        centralLayout.addWidget(self.image_viewer, 0, 0)

        self.tools_area = ToolsArea()
        self.tools_area.target_button.clicked.connect(self.image_viewer.setTargetMover)
        self.tools_area.grade_button.clicked.connect(self.image_viewer.setScoreUpdater)
        centralLayout.addWidget(self.tools_area, 0, 1)
