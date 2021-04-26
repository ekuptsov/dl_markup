from PyQt5 import QtGui, QtCore, QtWidgets


class CylinderItem(QtWidgets.QGraphicsItem):

    def __init__(
            self,
            begin: QtCore.QPointF,
            end: QtCore.QPointF,
            radius: float,
            pen: QtGui.QPen = None,
            brush: QtGui.QBrush = None):
        super().__init__()
        self.__begin = begin
        self.__end = end
        self.__radius = radius
        self.__pen = pen
        self.__brush = brush
        self.__create_parts()

    def __create_parts(self):
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
        self.__ellipse_1.setPen(self.__pen)
        self.__ellipse_1.setBrush(self.__brush)
        self.__ellipse_2.setPen(self.__pen)
        self.__ellipse_2.setBrush(self.__brush)
        self.__polygon.setPen(self.__pen)
        self.__polygon.setBrush(self.__brush)

    def boundingRect(self) -> QtCore.QRectF:
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
        return QtCore.QRectF(min(x), min(y), max(x), max(y))

    def paint(
            self,
            painter: QtGui.QPainter,
            option: QtWidgets.QStyleOptionGraphicsItem,
            widget: QtWidgets.QWidget):
        self.__ellipse_1.paint(painter, option, widget)
        self.__ellipse_2.paint(painter, option, widget)
        self.__polygon.paint(painter, option, widget)


class Scene(QtWidgets.QGraphicsScene):

    def __init__(self, *argc, **kwargs):
        super().__init__(*argc, **kwargs)
        self.__img_item = None
        self.setBackgroundBrush(QtGui.QBrush(
            QtGui.QColor(0, 0, 0)
        ))

    def __set_alpha(self, img: QtGui.QPixmap, alpha: float) -> QtGui.QPixmap:
        output = QtGui.QPixmap(img.size())
        output.fill(QtGui.QColor.fromRgb(0, 0, 0, 0))
        painter = QtGui.QPainter(output)
        painter.setOpacity(alpha)
        painter.drawPixmap(0, 0, img)
        painter.end()
        return output

    @property
    def img(self) -> QtGui.QPixmap:
        return self.__img_item.pixmap()

    @img.setter
    def img(self, val: QtGui.QPixmap):
        if self.__img_item is not None:
            self.removeItem(self.__img_item)
        img = self.__set_alpha(val, 0.8)
        self.__img_item = QtWidgets.QGraphicsPixmapItem(img)
        self.__img_item.setZValue(1.0)
        self.addItem(self.__img_item)

    @property
    def segm(self) -> QtGui.QPixmap:
        self.removeItem(self.__img_item)

        segm = QtGui.QPixmap(self.width(), self.height())
        segm.fill(QtGui.QColor.fromRgb(0, 0, 0, 0))
        painter = QtGui.QPainter(segm)
        self.render(painter)
        painter.end()

        self.addItem(self.__img_item)
        return segm
