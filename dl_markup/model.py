from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtGui
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

    def open(self, get_indexes):
        indexes = get_indexes()
        if indexes:
            index = indexes[0].row()
            img_path = os.path.join(
                self.inputDirectory.text(),
                self.listModel.items[index]
            )
            self.scene.img = QtGui.QPixmap(img_path)

    def save(self):
        print("Save called")

    def _updateFileList(self):
        files = os.listdir(self.inputDirectory.text())
        print("Updating file list:", files)
        self.listModel.setItems(files)