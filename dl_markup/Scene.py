from PyQt5 import QtGui, QtWidgets


class Scene(QtWidgets.QGraphicsScene):
    """Class that stores drawn primitives."""

    def __init__(self, *argc, **kwargs):
        """Initialize scene."""
        super().__init__(*argc, **kwargs)
        self.__img_item = None
        self.__background_item = None  # parent to all other items (except img)
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
        if self.__img_item is not None:
            self.removeItem(self.__img_item)
        super().clear()
        if self.__img_item is not None:
            self.addItem(self.__img_item)
            self.__background_item = self.__get_background_item(
                self.img.width(),
                self.img.height(),
            )
            self.addItem(self.__background_item)

    @property
    def img_item(self) -> QtWidgets.QGraphicsPixmapItem:
        """Drawing item with background image."""
        return self.__img_item

    @property
    def background_item(self) -> QtWidgets.QGraphicsPixmapItem:
        """Drawing item with empty background.

        This serves as parent for every other item (except actual background image)
        """
        return self.__background_item

    @property
    def img(self) -> QtGui.QPixmap:
        """Background image."""
        return self.__img_item.pixmap() if self.__img_item is not None else None

    @img.setter
    def img(self, val: QtGui.QPixmap):
        # remove current image item and background item
        child_items = []
        if self.__img_item is not None:
            child_items = self.__background_item.childItems()
            for item in child_items:
                item.setParentItem(None)
            self.removeItem(self.__img_item)
            self.removeItem(self.__background_item)
        # create new img item
        val = self.__set_alpha(val, 0.8)
        self.__img_item = self.__get_img_item(val)
        self.addItem(self.__img_item)
        # create background item and set its children
        self.__background_item = self.__get_background_item(
            val.width(),
            val.height(),
        )
        for item in child_items:
            item.setParentItem(self.__background_item)
        self.addItem(self.__background_item)
        # chage bounding rectangle accoring to new image size
        self.setSceneRect(0, 0, val.width(), val.height())

    def __get_img_item(self, img: QtGui.QPixmap) -> QtWidgets.QGraphicsPixmapItem:
        img_item = QtWidgets.QGraphicsPixmapItem(img)
        img_item .setZValue(1.0)
        return img_item

    def __get_background_item(self, width: int, height: int) -> QtWidgets.QGraphicsPixmapItem:
        background = QtGui.QPixmap(width, height)
        background.fill(QtGui.QColor(0, 0, 0))
        # set this flag to prevent drawing mask outside of image
        flag = QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemClipsChildrenToShape
        background_item = QtWidgets.QGraphicsPixmapItem(background)
        background_item.setFlag(flag)
        return background_item

    @property
    def segm(self) -> QtGui.QPixmap:
        """Return current segmentation mask."""
        self.removeItem(self.__img_item)

        segm = QtGui.QPixmap(self.width(), self.height())
        segm.fill(QtGui.QColor.fromRgb(0, 0, 0, 0))
        painter = QtGui.QPainter(segm)
        self.render(painter)
        painter.end()

        self.addItem(self.__img_item)
        return segm
