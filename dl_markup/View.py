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
        self._createToolbar(model, canvas)

        mainLayout = QVBoxLayout()

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        centralWidget.setLayout(mainLayout)

        inputBar, outputBar = self._createIOBar(model)
        mainLayout.addLayout(inputBar)
        mainLayout.addLayout(outputBar)

        layout = QHBoxLayout()
        mainLayout.addLayout(layout)

        # display list of images in input dir
        fileList = QListView()
        fileList.setModel(model.listModel)
        fileList.clicked.connect(
            partial(model.open, fileList.selectedIndexes))
        layout.addWidget(fileList)

        # painting area
        layout.addWidget(canvas)

        toolLayout = self._createToolLayout(canvas)
        layout.addLayout(toolLayout)

    def _createToolLayout(self, canvas: Canvas):
        """Store markup tools and color palette.

        Area lies to the right of canvas.
        """
        toolLayout = QVBoxLayout()
        toolLayout.addStretch(1)

        toolBox = QVBoxLayout()
        title = QLabel(
            QCoreApplication.translate('View', 'Markup tool'))
        title.setAlignment(Qt.AlignHCenter)
        toolBox.addWidget(title)
        # user switches between tools
        btLayout = QHBoxLayout()
        brush = QPushButton(
            QCoreApplication.translate('View', 'Brush'))
        polygon = QPushButton(
            QCoreApplication.translate('View', 'Polygon'))
        brush.setCheckable(True)
        polygon.setCheckable(True)
        # brush pressed by default
        brush.setChecked(True)
        # at each moment only one button is pressed
        buttons = [brush, polygon]
        slot = partial(canvas.changeTool, buttons)
        brush.clicked.connect(slot)
        brush.clicked.emit()
        polygon.clicked.connect(slot)
        btLayout.addWidget(brush)
        btLayout.addWidget(polygon)
        toolBox.addLayout(btLayout)
        toolLayout.addLayout(toolBox)
        # user choose tool color by pressing button on palette
        palette = Palette()
        palette.bindButtons(canvas)
        toolLayout.addWidget(palette)
        return toolLayout

    def _createIOBar(self, model: Model):
        """Create bar that display and change input and output directories.

        It lie above the canvas.
        """
        inputBar = QHBoxLayout()
        inputTitle = QLabel(
            QCoreApplication.translate('View', 'Input directory'))
        inputBar.addWidget(inputTitle)
        model.inputDirectory.editingFinished.connect(model.updateFileList)
        inputBar.addWidget(model.inputDirectory)
        changeInputDir = QPushButton(
            QCoreApplication.translate('View', 'Change'))
        changeInputDir.clicked.connect(model.selectInputDirectory)
        inputBar.addWidget(changeInputDir)

        outputBar = QHBoxLayout()
        outputTitle = QLabel(
            QCoreApplication.translate('View', 'Output directory'))
        outputBar.addWidget(outputTitle)
        outputBar.addWidget(model.outputDirectory)
        changeOutputDir = QPushButton(
            QCoreApplication.translate('View', 'Change'))
        changeOutputDir.clicked.connect(model.selectOutputDirectory)
        outputBar.addWidget(changeOutputDir)
        return inputBar, outputBar

    def _createToolbar(self, model: Model, canvas: Canvas):
        """Create toolbar with control buttons."""
        tools = QToolBar()
        self.addToolBar(tools)
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
