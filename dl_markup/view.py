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
        self.inputDirectory = QtWidgets.QLabel('.')
        self.outputDirectory = QtWidgets.QLabel('.')

        mainLayout = QtWidgets.QVBoxLayout()
        centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(centralWidget)
        centralWidget.setLayout(mainLayout)
        mainLayout.addWidget(self.inputDirectory)
        mainLayout.addWidget(self.outputDirectory)

        layout = QtWidgets.QHBoxLayout()
        mainLayout.addLayout(layout)
        layout.addWidget(self.fileList)
        layout.addWidget(QtWidgets.QGraphicsView(scene))

        self._createToolbar()

    def _createToolbar(self):
        tools = QtWidgets.QToolBar()
        self.addToolBar(tools)
        tools.addAction('Select input directory', self._selectInputDirectory)
        tools.addAction('Select output directory', self._selectOutputDirectory)
        tools.addAction('Save', print)

    def _selectInputDirectory(self):
        self.inputDirectory.setText(QtWidgets.QFileDialog.getExistingDirectory())

    def _selectOutputDirectory(self):
        self.outputDirectory.setText(QtWidgets.QFileDialog.getExistingDirectory())