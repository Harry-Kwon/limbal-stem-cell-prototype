from PySide2.QtWidgets import QScrollArea, QLabel, QWidget, QVBoxLayout, QGridLayout, QSlider, QPushButton
from PySide2.QtCore import Qt
from lsc.models import state
import numpy as np


class ToolsArea(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)

        container = QWidget()
        container.setLayout(QVBoxLayout(container))

        self.target_button: QPushButton = QPushButton("Move Target", container)
        container.layout().addWidget(self.target_button)

        container.layout().addWidget(self._target_sizer())

        self.grade_button: QPushButton = QPushButton("Grade", container)
        container.layout().addWidget(self.grade_button)

        container.layout().addStretch()

        self.setWidget(container)
    
    def _update_target_sizer(self):
        if state.image is not None:
            self.target_slider.setMaximum(np.max(state.image().shape))
        if state.target_radius is not None:
            self.target_slider.setValue(state.target_radius)

    def _target_sizer(self) -> QWidget:
        container = QWidget()
        layout = QGridLayout(container)
        container.setLayout(layout)

        label = QLabel("Target Size")
        layout.addWidget(label, 0, 0)

        self.target_slider = QSlider(container)
        self.target_slider.setMinimum(1)
        self.target_slider.setMaximum(500)
        self.target_slider.setTickInterval(1)
        self.target_slider.setOrientation(Qt.Horizontal)
        layout.addWidget(self.target_slider, 0,  1)
        self.target_slider.valueChanged.connect(self._set_target_radius)

        state.image_changed.connect(self._update_target_sizer)
        state.target_changed.connect(self._update_target_sizer)


        return container

    def _set_target_radius(self, val: int):
        state.target_radius = val
