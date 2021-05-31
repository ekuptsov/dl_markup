from PyQt5.QtWidgets import QWidget, QLabel, QSizePolicy
from PyQt5.QtWidgets import QGridLayout, QPushButton, QVBoxLayout

import math
from functools import partial

from .Canvas import Canvas


class Palette(QWidget):

    colors_hex = ['#00FF00', '#FFFFFF', '#FF0000', '#0000FF',
                  '#FFFF00', '#00FFFF', '#FF00FF', '#800000',
                  '#808000', '#008000', '#800080', '#000080']
    size = 100, 50

    def __init__(self, itemsInRow=4, parent=None):
        self.rows = math.ceil(len(self.colors_hex) // itemsInRow) + 1
        self.columns = itemsInRow
        self.pressedButton = None
        self.buttons = self.createButtons()

        super().__init__(parent)
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Color palette'))
        grid = QGridLayout()
        for idx, item in enumerate(self.buttons):
            i, j = idx // self.columns, idx % self.columns
            grid.addWidget(item, i, j)
        layout.addLayout(grid)
        self.setLayout(layout)

    def createButtons(self):
        w, h = self.size
        bsize = w // self.columns, h // self.rows
        buttons = []
        for color in self.colors_hex:
            button = QPushButton()
            button.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
            button.setMinimumSize(*bsize)
            button.setStyleSheet(f'background-color: {color};')
            buttons.append(button)
        return buttons

    def bindButtons(self, canvas: Canvas):
        color_change = canvas.changeToolColor
        for bt, color in zip(self.buttons, self.colors_hex):
            bt.setCheckable(True)
            bt.clicked.connect(self.changePressedButton)
            bt.clicked.connect(partial(color_change, f'{color}'))
            if color == '#00FF00':  # green is default color
                bt.setChecked(True)
                self.pressedButton = bt

    def changePressedButton(self):
        sender = self.sender()
        if self.pressedButton is not None:
            self.pressedButton.setChecked(False)
        self.pressedButton = sender
