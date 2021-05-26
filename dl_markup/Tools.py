from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QPixmap, QPainter

from .CylinderItem import CylinderItem


class Brush:

    def __init__(self, canvas):
        self.canvas = canvas
        self.color = QtGui.QColor(0, 255, 0)
        self.last_x, self.last_y = None, None
        self.mouse_pressed = False
        self.radius = 20

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = min(value, 63)
        # redraw cursor
        self.canvas.setCursor(self.cursor())

    @radius.deleter
    def radius(self):
        del self._radius

    def cursor(self):
        return self._CircleCursor()

    def _CircleCursor(self):
        """Draw a circle cursor of the same size as brush."""
        size = 128
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)

        # draw circle on pixmap
        painter = QPainter()
        painter.begin(pixmap)
        if hasattr(self.canvas, 'zoom'):
            diameter = self.radius * self.canvas.zoom * 2
        else:
            diameter = self.radius * 2
        left = (size - diameter) // 2
        top = (size - diameter) // 2
        # draw bbox in (left, top) with size (diameter, diameter)
        painter.drawEllipse(left, top, diameter, diameter)
        painter.end()
        return QCursor(pixmap)

    def mouseMoveEvent(self, e):
        """Draw cylinder between previous and current mouse positions.

        :param e: event object
        """
        canvas = self.canvas
        if canvas.scene.img_item is None:
            return
        if not self.mouse_pressed:
            return

        scene_point = canvas.mapToScene(e.pos())

        # cursor has moved outside of the scene
        if scene_point.x() < 0 or \
                scene_point.y() < 0 or \
                scene_point.x() > canvas.scene.width() - 1 or \
                scene_point.y() > canvas.scene.height() - 1:
            self.last_x, self.last_y = None, None
            return

        if self.last_x is None:  # First event.
            self.last_x = scene_point.x()
            self.last_y = scene_point.y()
            return  # Ignore the first time.

        cylinder = CylinderItem(
            QtCore.QPointF(self.last_x, self.last_y),
            QtCore.QPointF(scene_point.x(), scene_point.y()),
            self.radius,
            pen=QtGui.QPen(self.color),
            brush=QtGui.QBrush(self.color),
            parent=canvas.scene.background_item,
        )
        canvas.undo_redo.insert_in_undo_redo_add(cylinder)

        # Update the origin for next time.
        self.last_x = scene_point.x()
        self.last_y = scene_point.y()

    def mousePressEvent(self, e):
        scene_point = self.canvas.mapToScene(e.pos())
        self.last_x = scene_point.x()
        self.last_y = scene_point.y()
        self.mouse_pressed = True

    def mouseReleaseEvent(self, e):
        """Clear mouse position info.

        :param e: event object
        """
        self.last_x = None
        self.last_y = None
        self.mouse_pressed = False

    def keyPressEvent(self, e):
        """Change brush size by pressing '+' and '-' buttons.

        :param e: event object
        """
        if e.key() == Qt.Key_Plus or e.key() == Qt.Key_Equal:
            self.radius = self.radius + 1
        elif e.key() == Qt.Key_Minus:
            self.radius = max(1, self.radius - 1)
        else:
            return
        # self.setCursor(self._CircleCursor())
        print("New brush size:", self.radius)


class Polygon:
    def __init__(self, canvas):
        self.canvas = canvas
        self.color = QtGui.QColor(0, 255, 0)
        self.last_x, self.last_y = None, None
        self.mouse_pressed = False

    def mousePressEvent(self, e):
        """Add new vertex."""

    def mouseMoveEvent(self, e):
        """Draw a line that connect previous vertex and current mouse pos."""

    def cursor():
        return Qt.CrossCursor
