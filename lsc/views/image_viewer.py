from PySide2.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsPathItem
from PySide2.QtGui import QPixmap, QImage, QMouseEvent, QPainterPath, QPen, QColor, QResizeEvent, QFont, QBrush, QFontMetricsF
from PySide2.QtCore import Qt, QPoint, QPointF
import numpy as np
from lsc.models import state, grade_regions


class MouseStrategy:
    @staticmethod
    def mouse_move_event(e: QMouseEvent, p: QPoint):
        return

    @staticmethod
    def mouse_press_event(e: QMouseEvent, p: QPoint):
        return

    @staticmethod
    def mouse_release_event(e: QMouseEvent, p: QPoint):
        return


class TargetMover(MouseStrategy):
    @staticmethod
    def mouse_move_event(e: QMouseEvent, p: QPoint):
        if e.buttons() == Qt.LeftButton:
            state.target_position = tuple(int(x) for x in p.toTuple())


class ScoreUpdater(MouseStrategy):

    @staticmethod
    def mouse_press_event(e: QMouseEvent, p: QPoint):
        if e.buttons() == Qt.LeftButton:
            for region in grade_regions:
                x, y = tuple((a - b)/state.target_radius for (a, b) in zip(p.toTuple(), state.target_position))
                angle = np.rad2deg(np.arctan(y/x))
                radius = np.sqrt(x**2 + y**2)
                if region.contains_point(x, y):
                    region.increment_score()
        if e.buttons() == Qt.RightButton:
            for region in grade_regions:
                x, y = tuple((a - b)/state.target_radius for (a, b) in zip(p.toTuple(), state.target_position))
                angle = np.rad2deg(np.arctan(y/x))
                radius = np.sqrt(x**2 + y**2)
                if region.contains_point(x, y):
                    region.decrement_score()


class ImageViewer(QGraphicsView):
    _main_image: QGraphicsPixmapItem = None
    _target: QGraphicsPathItem = None
    _mouse_strategy: MouseStrategy = TargetMover

    def setTargetMover(self):
        self._mouse_strategy = TargetMover

    def setScoreUpdater(self):
        self._mouse_strategy = ScoreUpdater

    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene())
        self.setMouseTracking(True)

        state.image_changed.connect(self.update_image)
        state.target_changed.connect(self.update_target)
        for region in grade_regions:
            region.score_updated.connect(self.update_target)

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self.fitInView(self.sceneRect(),
                       aspectRadioMode=Qt.KeepAspectRatioByExpanding)

        if self._main_image is not None:
            self.setSceneRect(self._main_image.boundingRect())

    def update_image(self):
        pixmap: QPixmap = self._array_to_pixmap(state.image())
        if self._main_image is None:
            self._main_image = self.scene().addPixmap(pixmap)
        else:
            self._main_image.setPixmap(pixmap)
        self.fitInView(self.sceneRect(),
                       aspectRadioMode=Qt.KeepAspectRatioByExpanding)
        self.setSceneRect(self._main_image.boundingRect())

    def update_target(self):
        # generate target
        path = self._generate_target()
        grades = self._generate_grades()

        if self._target is None:
            self._target = self.scene().addPath(path)
            self._target.setPen(QPen(QColor(100, 255, 100, 200), 1))
            self._target.boundingRect = self._get_bounding_rect

            self._grades = self.scene().addPath(grades)
            self._grades.setPen(QPen(QColor(0, 0, 0, 100), 1))
            self._grades.setBrush(QBrush(QColor(255, 255, 255, 255)))
            self._grades.boundingRect = self._get_bounding_rect
        else:
            self._target.setPath(path)
            self._grades.setPath(grades)

    def _get_bounding_rect(self):
        if self._main_image is None:
            return None
        return self.sceneRect()

    def _generate_target(self) -> QPainterPath:
        path = QPainterPath()

        if state.target_position is None:
            return path

        r = state.target_radius
        x, y = state.target_position

        # generate radii
        radii = set([state.target_radius])

        # generate separators
        for region in grade_regions:
            # update radii
            radii.add(region.min_radius)
            radii.add(region.max_radius)

            # draw radii
            for angle in (region.min_angle, region.max_angle):
                c = np.cos(np.deg2rad(angle))
                s = np.sin(np.deg2rad(angle))

                start_x = int(r * region.min_radius * c)
                start_y = int(r * region.min_radius * s)
                end_x = int(r * region.max_radius * c)
                end_y = int(r * region.max_radius * s)

                path.moveTo(x+start_x, y+start_y)
                path.lineTo(x+end_x, y+end_y)

        # draw radii
        for gr in radii:
            path.addEllipse(x-r*gr, y-r*gr, 2*r*gr, 2*r*gr)

        return path
    
    def _generate_grades(self) -> QPainterPath:
        path = QPainterPath()

        if state.target_position is None:
            return path

        r = state.target_radius
        x, y = state.target_position

        # generate separators
        for region in grade_regions:
            # generate grade labels
            angle = (region.min_angle+region.max_angle)/2
            radius = (region.min_radius + region.max_radius)/2
            c = np.cos(np.deg2rad(angle))
            s = np.sin(np.deg2rad(angle))
            tx = int(r * radius * c)
            ty = int(r * radius * s)

            font = QFont()
            font.setPointSizeF(r/10)
            fw = QFontMetricsF(font).width(str(region.score))
            path.addText(x+tx-fw/2, y+ty+fw/2, font, str(region.score))

        return path

    def _array_to_pixmap(self, arr) -> QPixmap:
        """ Converts a numpy array to a pixmap.

        Args:
            arr (np.array): a numpy array representing an image
        """
        height, width, *channels = arr.shape
        channels = 1 if len(channels) == 0 else channels[0]
        if channels == 1:
            format = QImage.Format_Grayscale8
        elif channels == 3:
            format = QImage.Format_RGB888
        elif channels == 4:
            format = QImage.Format_RGBA8888
        qimage = QImage(np.ascontiguousarray(arr).data,
                        width, height, width*channels, format)
        qpixmap = QPixmap(qimage)
        return qpixmap

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        #        super().mouseMoveEvent(event)
        self._mouse_strategy.mouse_move_event(
            event, self.mapToScene(event.pos()))

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        #        super().mouseReleaseEvent(event)
        self._mouse_strategy.mouse_release_event(
            event, self.mapToScene(event.pos()))

    def mousePressEvent(self, event: QMouseEvent) -> None:
        #        super().mousePressEvent(event)
        self._mouse_strategy.mouse_press_event(
            event, self.mapToScene(event.pos()))
    
    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        self._mouse_strategy.mouse_press_event(
            event, self.mapToScene(event.pos()))