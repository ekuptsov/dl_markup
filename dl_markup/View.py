from PyQt5.QtWidgets import QListView
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import Qt

from functools import partial

from .Model import Model
from .Canvas import Canvas
from .Palette import Palette


class View(QMainWindow):
    """Application view according to MVC pattern."""

    def __init__(self, model: Model, canvas: Canvas):
        """Assemble UI from separate widgets.

        :param model: object that stores application data
        :param canvas: object for drawing
        """
        super().__init__()
        self.setWindowTitle("DL Markup")

        mainLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        centralWidget.setLayout(mainLayout)

        input_bar = QHBoxLayout()
        input_bar.addWidget(QLabel("Input directory"))
        model.inputDirectory.editingFinished.connect(model.updateFileList)
        input_bar.addWidget(model.inputDirectory)
        change_input_bt = QPushButton("Change")
        change_input_bt.clicked.connect(model.selectInputDirectory)
        input_bar.addWidget(change_input_bt)
        mainLayout.addLayout(input_bar)

        output_bar = QHBoxLayout()
        output_bar.addWidget(QLabel("Output directory"))
        output_bar.addWidget(model.outputDirectory)
        change_output_bt = QPushButton("Change")
        change_output_bt.clicked.connect(model.selectOutputDirectory)
        output_bar.addWidget(change_output_bt)
        mainLayout.addLayout(output_bar)

        layout = QHBoxLayout()
        mainLayout.addLayout(layout)

        fileList = QListView()
        fileList.setModel(model.listModel)
        fileList.clicked.connect(partial(model.open, fileList.selectedIndexes))
        layout.addWidget(fileList)

        layout.addWidget(canvas)

        self._createToolbar(model, canvas)

        right_layout = QVBoxLayout()
        right_layout.addStretch(1)
        mode = self._createModeButtons(canvas)
        right_layout.addLayout(mode)
        palette = Palette()
        palette.bindButtons(canvas)
        right_layout.addWidget(palette)
        layout.addLayout(right_layout)

    def _createModeButtons(self, canvas: Canvas):
        mode = QVBoxLayout()
        title = QLabel('Markup mode')
        title.setAlignment(Qt.AlignHCenter)
        mode.addWidget(title)
        bt_layout = QHBoxLayout()
        brush = QPushButton("Brush")
        polygon = QPushButton("Polygon")
        brush.setCheckable(True)
        polygon.setCheckable(True)
        brush.setChecked(True)
        buttons = [brush, polygon]
        slot = partial(canvas.changeTool, buttons)
        brush.clicked.connect(slot)
        brush.clicked.emit()
        polygon.clicked.connect(slot)
        bt_layout.addWidget(brush)
        bt_layout.addWidget(polygon)
        mode.addLayout(bt_layout)
        return mode

    def _createToolbar(self, model: Model, canvas: Canvas):
        """Create toolbar with control buttons."""
        tools = QToolBar()
        self.addToolBar(tools)
        # tools.addAction(
        #     QCoreApplication.translate('View', 'Select input directory'),
        #     model.selectInputDirectory
        # )
        # tools.addAction(
        #     QCoreApplication.translate('View', 'Select output directory'),
        #     model.selectOutputDirectory
        # )
        # tools.addAction(
        #     QCoreApplication.translate('View', 'Open'),
        #     partial(model.open, self.fileList.selectedIndexes)
        # )
        tools.addAction(
            QCoreApplication.translate('View', 'Save'),
            model.save
        )
        tools.addAction(
            QCoreApplication.translate('View', 'Undo'),
            partial(canvas.undo_redo.undo, levels=1)
        )
        tools.addAction(
            QCoreApplication.translate('View', 'Redo'),
            partial(canvas.undo_redo.redo, levels=1)
        )
        tools.addAction(
            QCoreApplication.translate('View', 'Clear'),
            canvas.clear
        )
