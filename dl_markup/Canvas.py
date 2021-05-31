from PyQt5 import QtGui, QtCore, QtWidgets
# from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QCursor, QPixmap, QPainter

# from .CylinderItem import CylinderItem
from .Scene import Scene
from .UndoRedo import UndoRedo
from .Tools import Brush, Polygon


class Canvas(QtWidgets.QGraphicsView):
    """A class capable of user interaction with scene.

    Inherits QtWidgets.QGraphicsView, so it can be placed in layout.
    Store scene, undo_redo module and available tools.
    """

    def __init__(self, scene: Scene, undo_redo: UndoRedo):
        """Create a new canvas.

        :param scene: scene object for drawing
        :param undo_redo: an object for storing history
        """
        super().__init__(scene)
        self.scene = scene
        self.undo_redo = undo_redo
        # self.tool = Brush(self)
        self.tool = Polygon(self)
        self.setCursor(self.tool.cursor())

        self.zoom = 1.
        self.zoom_factor = 1.04

    def mouseMoveEvent(self, e):
        super().mouseMoveEvent(e)
        self.tool.mouseMoveEvent(e)

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        self.tool.mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        """Clear mouse position info.

        :param e: event object
        """
        super().mouseReleaseEvent(e)
        self.tool.mouseReleaseEvent(e)

    def keyPressEvent(self, e):
        """Change brush size by pressing '+' and '-' buttons.

        :param e: event object
        """
        super().keyPressEvent(e)
        self.tool.keyPressEvent(e)

    def changeTool(self, buttons):
        sender = self.sender()
        prev_button = buttons[sender == buttons[0]]
        prev_button.setChecked(False)

    def changeToolColor(self, color: str):
        self.tool.color = QtGui.QColor(color)

    def _zoom(self, angle_delta: QtCore.QPointF):
        # set new anchor
        old_anchor = self.transformationAnchor()
        new_anchor = QtWidgets.QGraphicsView.ViewportAnchor.AnchorViewCenter
        self.setTransformationAnchor(new_anchor)

        # zoom
        zoom_factor = self.zoom_factor
        if angle_delta.y() < 0:
            zoom_factor = 1 / self.zoom_factor
        self.zoom *= zoom_factor
        self.scale(zoom_factor, zoom_factor)
        # dont forget about cursor
        self.setCursor(self.tool.cursor())
        # reset old anchor
        self.setTransformationAnchor(old_anchor)

    def wheelEvent(self, e):
        if e.modifiers() & QtCore.Qt.ControlModifier:
            self._zoom(e.angleDelta())
        else:
            super().wheelEvent(e)

    def clear(self):
        """Clear scene and history."""
        self.scene.clear()
        self.undo_redo.clear()

    def updateBackgroundImage(self, img_path: str):
        """Update background image with clearing current segmentation.

        :param img_path: path to new background image
        """
        self.clear()
        self.scene.img = QtGui.QPixmap(img_path)
