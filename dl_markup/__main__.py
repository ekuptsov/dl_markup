from PyQt5 import QtGui, QtCore, QtWidgets

from .undo_redo import UndoRedo
from .scene import Scene, CylinderItem


def main():
    app = QtWidgets.QApplication([])

    scene = Scene(0, 0, 512, 512)
    scene.img = QtGui.QPixmap('resources/Lenna.png')
    undo_redo = UndoRedo(scene)

    cylinder = CylinderItem(
        QtCore.QPointF(100, 100),
        QtCore.QPointF(200, 200),
        20,
        pen=QtGui.QPen(QtGui.QColor(0, 255, 0)),
        brush=QtGui.QBrush(QtGui.QColor(0, 255, 0))
    )

    undo_redo.insert_in_undo_redo_add(cylinder)

    view = QtWidgets.QGraphicsView(scene)
    view.show()

    view.show()
    app.exec_()
