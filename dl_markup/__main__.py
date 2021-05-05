from PyQt5 import QtWidgets
from PyQt5.QtCore import QTranslator
import locale

from .undo_redo import UndoRedo
from .scene import Scene
from .view import View
from .model import Model
from .canvas import Canvas


def main():
    app = QtWidgets.QApplication([])

    locale_str = locale.getlocale(locale.LC_MESSAGES)[0]
    translator = QTranslator()
    translator.load(f"dl_markup.{locale_str}")
    if not app.installTranslator(translator):
        print("Can not install translation")

    scene = Scene(0, 0, 512, 512)
    undo_redo = UndoRedo(scene)
    canvas = Canvas(scene, undo_redo)
    model = Model(canvas)
    view = View(model, canvas)
    view.show()
    app.exec_()
