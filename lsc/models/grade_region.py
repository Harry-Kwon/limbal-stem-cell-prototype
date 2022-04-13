from PySide2.QtCore import QObject, Signal
import numpy as np

class GradeRegion(QObject):
    _max_score = 5

    min_angle: float
    max_angle: float

    min_radius: float
    max_radius: float

    _score: int = 0
    score_updated: Signal = Signal(int)
    @property
    def score(self) -> int:
        return self._score

    def __init__(self, min_angle, max_angle, min_radius, max_radius):
        super().__init__()
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.min_radius = min_radius
        self.max_radius = max_radius
    
    def increment_score(self):
        self._score = (self._score+1)%GradeRegion._max_score
        self.score_updated.emit(self._score)

    def decrement_score(self):
        self._score = (self._score-1)%GradeRegion._max_score
        self.score_updated.emit(self._score)
    
    def contains_point(self, x, y):
        radius = np.sqrt(x**2 + y**2)
        angle = np.rad2deg(np.arctan(y/x))
        if x>=0 and y>=0:
            pass
        elif x<=0 and y>=0:
            angle = 180 + angle
        elif x<=0 and y <= 0:
            angle = 180 + angle
        elif x>=0 and y <= 0:
            angle = 360+angle

        contained = True
        contained = contained and angle >= self.min_angle
        contained = contained and angle <= self.max_angle
        contained = contained and radius >= self.min_radius
        contained = contained and radius <= self.max_radius
        return contained