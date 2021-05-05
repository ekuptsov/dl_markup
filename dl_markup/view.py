from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QListView
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMainWindow
import os

from .list_model import ListModel


class View(QMainWindow):
    """
    Application view
    """
    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self.listModel = ListModel()
        self.fileList = QListView()
        self.fileList.setModel(self.listModel)
        self.setWindowTitle("DL Markup")
        self.inputDirectory = QLabel('.')
        self.outputDirectory = QLabel('.')

        mainLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        centralWidget.setLayout(mainLayout)
        mainLayout.addWidget(self.inputDirectory)
        mainLayout.addWidget(self.outputDirectory)

        layout = QHBoxLayout()
        mainLayout.addLayout(layout)
        layout.addWidget(self.fileList)
        layout.addWidget(QGraphicsView(scene))

        self._createToolbar()

    def _createToolbar(self):
        tools = QToolBar()
        self.addToolBar(tools)
        tools.addAction('Select input directory', self._selectInputDirectory)
        tools.addAction('Select output directory', self._selectOutputDirectory)
        tools.addAction('Open', self._open)
        tools.addAction('Save', self._save)

    def _selectInputDirectory(self):
        self.inputDirectory.setText(QFileDialog.getExistingDirectory())
        self._updateFileList()

    def _selectOutputDirectory(self):
        self.outputDirectory.setText(QFileDialog.getExistingDirectory())

    def _open(self):
        pass

    def _save(self):
        pass

    def _updateFileList(self):
        files = os.listdir(self.inputDirectory.text())
        print("Updating file list:", files)
        self.listModel.setItems(files)