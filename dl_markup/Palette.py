from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import Qt

import math
from functools import partial

from .Canvas import Canvas


class Palette(QWidget):
    """Color palette.

    Hold buttons with available colors for tool.
    Developoed as single Widget without Model-View decomposition.
    """

    colors_hex = ['#00FF00', '#FFFFFF', '#FF0000', '#0000FF',
                  '#FFFF00', '#00FFFF', '#FF00FF', '#800000',
                  '#808000', '#008000', '#800080', '#000080']
    size = 100, 50

    def __init__(self, itemsInRow: int = 4, parent: QWidget = None):
        """Inittialize Palette.

        Palette fit buttons in grid.
        :param itemsInRow: number of buttons in each row
        :param parent: parent layout object
        """
        self.rows = math.ceil(len(self.colors_hex) // itemsInRow) + 1
        self.columns = itemsInRow
        self.pressedButton = None
        self.buttons = self.createButtons()

        super().__init__(parent)
        layout = QVBoxLayout()
        title = QLabel(
            QCoreApplication.translate('Palette', 'Color palette'))
        title.setAlignment(Qt.AlignHCenter)
        layout.addWidget(title)
        grid = QGridLayout()
        for idx, item in enumerate(self.buttons):
            i, j = idx // self.columns, idx % self.columns
            grid.addWidget(item, i, j)
        layout.addLayout(grid)
        self.setLayout(layout)

    def createButtons(self):
        """Create buttons with right size (palette size is fixed)."""
        w, h = self.size
        bsize = w // self.columns, h // self.rows
        buttons = []
        for color in self.colors_hex:
            button = QPushButton()
            button.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
            button.setMinimumSize(*bsize)
            style = """
                QPushButton {
                    background: """ + f'{color}' + """ ;}
                QPushButton::checked {
                    border: 3px solid black;}"""
            button.setStyleSheet(style)
            buttons.append(button)
        return buttons

    def bindButtons(self, canvas: Canvas):
        """Connect button color with canvas."""
        color_change = canvas.changeToolColor
        for bt, color in zip(self.buttons, self.colors_hex):
            bt.setCheckable(True)
            bt.clicked.connect(self.changePressedButton)
            bt.clicked.connect(partial(color_change, f'{color}'))
            # green is default color
            if color == '#00FF00':
                bt.setChecked(True)
                self.pressedButton = bt
                self.pressedButton.setEnabled(False)

    def changePressedButton(self):
        """Each time only one button is pressed."""
        sender = self.sender()
        if self.pressedButton is not None and sender is not self.pressedButton:
            self.pressedButton.setEnabled(True)
            self.pressedButton.setChecked(False)
        self.pressedButton = sender
        self.pressedButton.setEnabled(False)
