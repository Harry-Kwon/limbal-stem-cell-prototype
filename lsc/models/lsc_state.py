from typing import Tuple
import numpy as np
import cv2 as cv2
from PySide2.QtCore import QObject, Signal

class LSCState(QObject):
    """Global singleton for application state"""
    _instance: object = None

    current_file: str = None

    image_changed: Signal = Signal()
    _image: np.ndarray = None

    target_changed: Signal = Signal()
    _target_position = None
    _target_radius: int = 100

    @property
    def target_position(self) -> Tuple[int, int]:
        return self._target_position
    @target_position.setter
    def target_position(self, value: Tuple[int, int]):
        self._target_position = value
        self.target_changed.emit()

    @property
    def target_radius(self) -> int:
        return self._target_radius
    @target_radius.setter
    def target_radius(self, value: int):
        self._target_radius = value
        self.target_changed.emit()

    def __new__(cls):
        # only create a new object if there is not exiting instance
        if cls._instance is None:
            cls._instance = super(LSCState, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()

    def load_image(self, path: str) -> bool:
        self.current_file = path
        try:
            self._image = cv2.imread(path)
            self.image_changed.emit()

            self.target_position = (self._image.shape[1], self._image.shape[0])
            return True
        except Exception as e:
            print(e)
            return False
    
    def image(self) -> np.ndarray:
        return self._image