from PyQt5 import QtGui, QtCore, QtWidgets

class Canvas(QtWidgets.QGraphicsView):
    def __init__(self, scene, undo_redo):
        super().__init__(scene)
        self.undo_redo = undo_redo
