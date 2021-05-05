from PyQt5.QtWidgets import QListView
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QMainWindow

from functools import partial
from .model import Model
from .canvas import Canvas


class View(QMainWindow):
    """
    Application view
    """
    def __init__(self, model: Model, canvas: Canvas):
        super().__init__()
        self.setWindowTitle("DL Markup")

        mainLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        centralWidget.setLayout(mainLayout)

        mainLayout.addWidget(model.inputDirectory)
        mainLayout.addWidget(model.outputDirectory)

        layout = QHBoxLayout()
        mainLayout.addLayout(layout)

        self.fileList = QListView()
        self.fileList.setModel(model.listModel)
        layout.addWidget(self.fileList)

        layout.addWidget(canvas)

        self._createToolbar(model)

    def _createToolbar(self, model: Model):
        tools = QToolBar()
        self.addToolBar(tools)
        tools.addAction('Select input directory', model.selectInputDirectory)
        tools.addAction('Select output directory', model.selectOutputDirectory)
        openHandler = partial(model.open, self.fileList.selectedIndexes)
        tools.addAction('Open', openHandler)
        tools.addAction('Save', model.save)
