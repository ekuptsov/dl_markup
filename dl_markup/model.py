from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QFileDialog
import os

from .list_model import ListModel


class Model:
    def __init__(self, scene):
        self.scene = scene
        self.inputDirectory = QLabel('.')
        self.outputDirectory = QLabel('.')
        self.listModel = ListModel()

    def selectInputDirectory(self):
        self.inputDirectory.setText(QFileDialog.getExistingDirectory())
        self._updateFileList()

    def selectOutputDirectory(self):
        self.outputDirectory.setText(QFileDialog.getExistingDirectory())

    def open(self):
        pass

    def save(self):
        pass

    def _updateFileList(self):
        files = os.listdir(self.inputDirectory.text())
        print("Updating file list:", files)
        self.listModel.setItems(files)