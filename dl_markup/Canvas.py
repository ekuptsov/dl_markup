from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt

from .CylinderItem import CylinderItem
from .Scene import Scene
from .UndoRedo import UndoRedo


class Canvas(QtWidgets.QGraphicsView):
    """A class capable of user interaction with scene.

    Inherits QtWidgets.QGraphicsView, so it can be placed in layout.
    """

    def __init__(self, scene: Scene, undo_redo: UndoRedo):
        """Create a new canvas.

        :param scene: scene object for drawing
        :param undo_redo: an object for storing history
        """
        super().__init__(scene)
        self.scene = scene
        self.undo_redo = undo_redo
        self.color = QtGui.QColor(0, 255, 0)
        self.brush_size = 20
        self.last_x, self.last_y = None, None
        self.zoom_factor = 1.04
        self.mouse_pressed = False

    def mouseMoveEvent(self, e):
        """Draw cylinder between previous and current mouse positions.

        :param e: event object
        """
        if self.scene.img_item is None:
            return
        if not self.mouse_pressed:
            return

        scene_point = self.mapToScene(e.pos())

        # cursor has moved outside of the scene
        if scene_point.x() < 0 or \
                scene_point.y() < 0 or \
                scene_point.x() > self.scene.width() - 1 or \
                scene_point.y() > self.scene.height() - 1:
            self.last_x, self.last_y = None, None
            return

        if self.last_x is None:  # First event.
            self.last_x = scene_point.x()
            self.last_y = scene_point.y()
            return  # Ignore the first time.

        cylinder = CylinderItem(
            QtCore.QPointF(self.last_x, self.last_y),
            QtCore.QPointF(scene_point.x(), scene_point.y()),
            self.brush_size,
            pen=QtGui.QPen(self.color),
            brush=QtGui.QBrush(self.color),
            parent=self.scene.background_item,
        )
        self.undo_redo.insert_in_undo_redo_add(cylinder)

        # Update the origin for next time.
        self.last_x = scene_point.x()
        self.last_y = scene_point.y()

    def mousePressEvent(self, e):
        scene_point = self.mapToScene(e.pos())
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
            self.brush_size = self.brush_size + 1
        elif e.key() == Qt.Key_Minus:
            self.brush_size = max(1, self.brush_size - 1)
        else:
            return
        print("New brush size:", self.brush_size)

    def wheelEvent(self, e):
        if e.modifiers() & QtCore.Qt.ControlModifier:
            self._zoom(e.angleDelta())
        else:
            super().wheelEvent(e)

    def _zoom(self, angle_delta: QtCore.QPointF):
        # set new anchor
        old_anchor = self.transformationAnchor()
        new_anchor = QtWidgets.QGraphicsView.ViewportAnchor.AnchorViewCenter
        self.setTransformationAnchor(new_anchor)

        # zoom
        zoom_factor = self.zoom_factor
        if angle_delta.y() < 0:
            zoom_factor = 1 / self.zoom_factor
        self.scale(zoom_factor, zoom_factor)

        # reset old anchor
        self.setTransformationAnchor(old_anchor)

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
