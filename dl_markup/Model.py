from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QModelIndex

import os
import typing

from .ListModel import ListModel
from .Canvas import Canvas


class Model:
    """Store application model according to MVC pattern."""

    # def __init__(self, canvas: Canvas, input_dir: str, output_dir: str):
    def __init__(self, canvas: Canvas, input_dir: str = None, output_dir: str = None):
        """Initialize all data objects.

        :param canvas: Canvas object for drawing
        """
        self.canvas = canvas
        self.inputDirectory = QLabel(input_dir)
        self.outputDirectory = QLabel(output_dir)
        self.listModel = ListModel()
        self.workingImageName = None
        if input_dir is not None:
            self.updateFileList()

    def selectInputDirectory(self):
        """Select input directory by file dialog."""
        text = QFileDialog.getExistingDirectory()
        if text:
            self.inputDirectory.setText(text)
            self.updateFileList()

    def selectOutputDirectory(self):
        """Select output directory by file dialog."""
        text = QFileDialog.getExistingDirectory()
        if text:
            self.outputDirectory.setText(text)

    def open(self, get_indexes: typing.Callable[[], typing.List[QModelIndex]]):
        """Load selected image to canvas.

        :param get_indexes: function, which produces indexes of selected items
        """
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
        """Save segmentation to file."""
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

    def updateFileList(self):
        """Update list of files in selected input directory."""
        text = self.inputDirectory.text()
        if not text:
            return
        files = os.listdir(text)
        print("Updating file list:", files)
        self.listModel.setItems(files)
