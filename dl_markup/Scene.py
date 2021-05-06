from PyQt5 import QtGui, QtWidgets


class Scene(QtWidgets.QGraphicsScene):
    """Class that stores drawn primitives."""

    def __init__(self, *argc, **kwargs):
        """Initialize scene."""
        super().__init__(*argc, **kwargs)
        self.__img_item = None
        self.setBackgroundBrush(QtGui.QBrush(
            QtGui.QColor(0, 0, 0)
        ))

    def __set_alpha(self, img: QtGui.QPixmap, alpha: float) -> QtGui.QPixmap:
        """Create new image with another opacity.

        :param img: original image
        :param alpha: opacity value from interval [0, 1]
        """
        output = QtGui.QPixmap(img.size())
        output.fill(QtGui.QColor.fromRgb(0, 0, 0, 0))
        painter = QtGui.QPainter(output)
        painter.setOpacity(alpha)
        painter.drawPixmap(0, 0, img)
        painter.end()
        return output

    def clear(self):
        """Remove all primitives from scene, leaving background image."""
        img = self.img
        super().clear()
        if img is not None:
            self.__img_item = self.__get_img_item(img)
            self.addItem(self.__img_item)

    @property
    def img_item(self) -> QtWidgets.QGraphicsItem:
        return self.__img_item

    @property
    def img(self) -> QtGui.QPixmap:
        """Background image."""
        return self.__img_item.pixmap() if self.__img_item is not None else None

    @img.setter
    def img(self, val: QtGui.QPixmap):
        child_items = []
        if self.__img_item is not None:
            child_items = self.__img_item.childItems()
            for item in child_items:
                item.setParentItem(None)
            self.removeItem(self.__img_item)
        val = self.__set_alpha(val, 0.8)
        self.__img_item = self.__get_img_item(val)
        for item in child_items:
            item.setParentItem(self.__img_item)
        self.addItem(self.__img_item)

    def __get_img_item(self, img: QtGui.QPixmap) -> QtWidgets.QGraphicsPixmapItem:
        img_item = QtWidgets.QGraphicsPixmapItem(img)
        img_item .setZValue(1.0)
        flag = QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemClipsChildrenToShape
        img_item.setFlag(flag)
        return img_item

    @property
    def segm(self) -> QtGui.QPixmap:
        """Return current segmentation mask."""
        child_items = self.__img_item.childItems()
        for item in child_items:
            item.setParentItem(None)
        self.removeItem(self.__img_item)

        segm = QtGui.QPixmap(self.width(), self.height())
        segm.fill(QtGui.QColor.fromRgb(0, 0, 0, 0))
        painter = QtGui.QPainter(segm)
        self.render(painter)
        painter.end()

        self.addItem(self.__img_item)
        for item in child_items:
            item.setParentItem(self.__img_item)
        return segm
