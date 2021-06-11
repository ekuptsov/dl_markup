from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QPixmap, QPainter

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .Canvas import Canvas


class CylinderItem(QtWidgets.QGraphicsItem):
    """Drawing item that represents basic brush movement.

    Contains two circles and rectangle between them.
    """

    def __init__(
            self,
            begin: QtCore.QPointF,
            end: QtCore.QPointF,
            radius: float,
            pen: QtGui.QPen = None,
            brush: QtGui.QBrush = None,
            *args,
            **kwargs):
        """Initialize CylinderItem.

        :param begin: first point
        :param end: second point
        :param radius: size of circles
        :param pen: QPen object with color information
        :param brush: QBrush object with color information
        """
        super().__init__(*args, **kwargs)
        self.__begin = begin
        self.__end = end
        self.__radius = radius
        self.__pen = pen
        self.__brush = brush
        self.__create_parts()
        self.__compute_bounding_rect()

    def __create_parts(self):
        """Create circles and rectangle."""
        dir_vec = QtGui.QVector2D(
            self.__end.x() - self.__begin.x(),
            self.__end.y() - self.__begin.y()
        )
        dir_vec.normalize()
        norm_vec = QtGui.QVector2D(
            -dir_vec.y(),
            dir_vec.x()
        )
        vecs = [
            QtGui.QVector2D(self.__begin) + self.__radius*norm_vec,
            QtGui.QVector2D(self.__end) + self.__radius*norm_vec,
            QtGui.QVector2D(self.__end) - self.__radius*norm_vec,
            QtGui.QVector2D(self.__begin) - self.__radius*norm_vec,
        ]
        self.__polygon = QtWidgets.QGraphicsPolygonItem(
            QtGui.QPolygonF([QtCore.QPointF(vec.x(), vec.y()) for vec in vecs])
        )
        self.__ellipse_1 = QtWidgets.QGraphicsEllipseItem(
            self.__begin.x() - self.__radius,
            self.__begin.y() - self.__radius,
            2 * self.__radius,
            2 * self.__radius
        )
        self.__ellipse_2 = QtWidgets.QGraphicsEllipseItem(
            self.__end.x() - self.__radius,
            self.__end.y() - self.__radius,
            2 * self.__radius,
            2 * self.__radius
        )
        for item in (self.__ellipse_1, self.__ellipse_2, self.__polygon):
            item.setPen(self.__pen)
            item.setBrush(self.__brush)

    def __compute_bounding_rect(self):
        x = [
            self.__begin.x() - self.__radius,
            self.__begin.x() + self.__radius,
            self.__end.x() - self.__radius,
            self.__end.x() + self.__radius,
        ]
        y = [
            self.__begin.y() - self.__radius,
            self.__begin.y() + self.__radius,
            self.__end.y() - self.__radius,
            self.__end.y() + self.__radius,
        ]
        self.__bounding_rect = QtCore.QRectF(min(x), min(y), max(x), max(y))

    def boundingRect(self) -> QtCore.QRectF:
        """Create bounding box for current item."""
        return self.__bounding_rect

    def paint(
            self,
            painter: QtGui.QPainter,
            option: QtWidgets.QStyleOptionGraphicsItem,
            widget: QtWidgets.QWidget):
        """Paint item."""
        for item in (self.__ellipse_1, self.__ellipse_2, self.__polygon):
            item.paint(painter, option, widget)


class Brush:
    """Round markup tool which cursor size fits the width of drawing line.

    Draw CylinderItems when user hold and move the mouse on canvas.
    """
    def __init__(self, canvas: 'Canvas', color: QtGui.QColor):
        """Initialize brush.

        :param canvas: сanvas object for drawing
        :param color: color of brush
        """
        self.canvas = canvas
        self.color = color
        self.last_x, self.last_y = None, None
        self.mouse_pressed = False
        self.radius = 20

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        """Control max brush size and update cursor on canvas."""
        self._radius = max(min(value, 25), 2)
        self.canvas.setCursor(self.cursor())

    @radius.deleter
    def radius(self):
        del self._radius

    def cursor(self):
        """Each call redraw cursor.

        Every tool has unique cursor, which is updated (redrawn)
        after zooming, size changing or switching between tools.
        """
        return self._CircleCursor()

    def _CircleCursor(self):
        """Draw a circle cursor of the same size as brush."""
        pixmap_size = 128
        pixmap = QPixmap(pixmap_size, pixmap_size)
        pixmap.fill(Qt.GlobalColor.transparent)

        # draw circle on pixmap among .begin() and .end() calls
        painter = QPainter()
        painter.begin(pixmap)
        if hasattr(self.canvas, 'zoom'):
            diameter = self.radius * self.canvas.zoom * 2
            if diameter > pixmap_size:
                print(f"Max displayed diameter {pixmap_size}")
        else:
            diameter = self.radius * 2
        left = (pixmap_size - diameter) // 2
        top = (pixmap_size - diameter) // 2
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
        print("New brush size:", self.radius)
