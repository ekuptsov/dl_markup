from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt
from .cylinder_item import CylinderItem
from .scene import Scene
from .undo_redo import UndoRedo


class Canvas(QtWidgets.QGraphicsView):

    def __init__(self, scene: Scene, undo_redo: UndoRedo):
        super().__init__(scene)
        self.scene = scene
        self.undo_redo = undo_redo
        self.color = QtGui.QColor(0, 255, 0)
        self.brush_size = 20
        self.last_x, self.last_y = None, None

    def mouseMoveEvent(self, e):
        if self.last_x is None:  # First event.
            self.last_x = e.x()
            self.last_y = e.y()
            return  # Ignore the first time.

        cylinder = CylinderItem(
            QtCore.QPointF(self.last_x, self.last_y),
            QtCore.QPointF(e.x(), e.y()),
            self.brush_size,
            pen=QtGui.QPen(self.color),
            brush=QtGui.QBrush(self.color)
        )
        self.undo_redo.insert_in_undo_redo_add(cylinder)

        # Update the origin for next time.
        self.last_x = e.x()
        self.last_y = e.y()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Plus or e.key() == Qt.Key_Equal:
            self.brush_size = self.brush_size + 1
        elif e.key() == Qt.Key_Minus:
            self.brush_size = max(1, self.brush_size - 1)
        else:
            return
        print("New brush size:", self.brush_size)

    def clear(self):
        self.scene.clear()
        self.undo_redo.clear()

    def updateBackgroundImage(self, img_path: str):
        self.clear()
        self.scene.img = QtGui.QPixmap(img_path)
