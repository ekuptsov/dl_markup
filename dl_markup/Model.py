from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QModelIndex

import os
import typing
import re

from .ListModel import ListModel
from .Canvas import Canvas


class Model:
    """Store application model according to MVC pattern."""

    IMAGES_RE = re.compile(r'\w+.(?:jpg|jpeg|png|bmp)')

    def __init__(self, canvas: Canvas, input_dir: str, output_dir: str):
        """Initialize all data objects.

        :param canvas: Canvas object for drawing
        :param input_dir: Directory of images for markup
        :param output_dir: Directory of saved image segmentation mask
        """
        self.canvas = canvas
        self.saved_items = self.canvas.scene.items()
        self.inputDirectory = QLineEdit(os.path.abspath(input_dir))
        self.outputDirectory = QLineEdit(os.path.abspath(output_dir))
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

        If image has already opened, nothing is changed.
        If image have unsaved changes, MessageBox is poped up.
        :param get_indexes: function, which produces indexes of selected items
        """
        self.have_unsaved_changes()
        indexes = get_indexes()
        if indexes:
            index = indexes[0].row()
            if self.workingImageName != self.listModel.items[index]:
                self.workingImageName = self.listModel.items[index]
                img_path = os.path.join(
                    self.inputDirectory.text(),
                    self.workingImageName
                )
                print("Reading image from", img_path)
                self.canvas.updateBackgroundImage(img_path)
                self.saved_items = self.canvas.scene.items()

    def have_unsaved_changes(self):
        """Check if current items on canvas are the same as saved before.

        Otherwise pop up a MessageBox box with suggestion to save image.
        """
        items = self.canvas.scene.items()
        if self.saved_items != items:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Question)
            msg.setText("The image has been modified.")
            msg.setInformativeText("Do you want to save your changes?")
            msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            ret = msg.exec_()
            if ret == QMessageBox.Yes:
                self.save()

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
        self.saved_items = self.canvas.scene.items()

    def updateFileList(self):
        """Update list of files in selected input directory."""
        text = self.inputDirectory.text()
        if not text:
            return
        files = [file for file in os.listdir(text)
                 if re.fullmatch(self.IMAGES_RE, file)]
        print("Updating file list:", files)
        self.listModel.setItems(files)
