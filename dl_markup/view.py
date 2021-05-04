from PyQt5 import QtWidgets


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