from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtGui
import os

from .list_model import ListModel


class Model:
    def __init__(self, canvas):
        self.canvas = canvas
        self.inputDirectory = QLabel('.')
        self.outputDirectory = QLabel('.')
        self.listModel = ListModel()
        self.workingImageName = None

    def selectInputDirectory(self):
        self.inputDirectory.setText(QFileDialog.getExistingDirectory())
        self._updateFileList()

    def selectOutputDirectory(self):
        self.outputDirectory.setText(QFileDialog.getExistingDirectory())

    def open(self, get_indexes):
        indexes = get_indexes()
        if indexes:
            index = indexes[0].row()
            self.workingImageName = self.listModel.items[index]
            img_path = os.path.join(
                self.inputDirectory.text(),
                self.workingImageName
            )
            print("Reading image from", img_path)
            self.canvas.updateBackgroundImage(img_path)

    def save(self):
        print("Save called")
        if self.workingImageName is None:
            print("Working image is unknown. Skip saving.")
            return
        segm = self.canvas.scene.segm
        out_path = os.path.join(
                self.outputDirectory.text(),
                self.workingImageName
        )
        print("Saving image to", out_path)
        segm.save(out_path)

    def _updateFileList(self):
        files = os.listdir(self.inputDirectory.text())
        print("Updating file list:", files)
        self.listModel.setItems(files)