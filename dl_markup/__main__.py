from PyQt5 import QtGui, QtCore, QtWidgets

from .undo_redo import UndoRedo
from .scene import Scene, CylinderItem


class View(QtWidgets.QMainWindow):
    """
    Application view
    """
    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self.fileList = QtWidgets.QListView()
        self.setWindowTitle("DL Markup")
        self.generalLayout = QtWidgets.QHBoxLayout()
        self._centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        self.generalLayout.addWidget(self.fileList)
        self.generalLayout.addWidget(QtWidgets.QGraphicsView(scene))
        self._createToolbar()

    def _createToolbar(self):
        tools = QtWidgets.QToolBar()
        self.addToolBar(tools)
        tools.addAction('Select input directory', print)
        tools.addAction('Select output directory', print)
        tools.addAction('Save', print)


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

    view = View(scene)
    view.show()



    app.exec_()
