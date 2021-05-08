from PyQt5 import QtGui, QtCore, QtWidgets


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
        :param raduis: size of circles
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
