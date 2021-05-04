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
        self.inputDirectory = '.'
        self.outputDirectory = '.'
        layout = QtWidgets.QHBoxLayout()
        centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(centralWidget)
        centralWidget.setLayout(layout)
        layout.addWidget(self.fileList)
        layout.addWidget(QtWidgets.QGraphicsView(scene))
        self._createToolbar()

    def _createToolbar(self):
        tools = QtWidgets.QToolBar()
        self.addToolBar(tools)
        tools.addAction('Select input directory', print)
        tools.addAction('Select output directory', print)
        tools.addAction('Save', print)