from PyQt5 import QtWidgets
from PyQt5.QtCore import QTranslator

import locale

from .UndoRedo import UndoRedo
from .Scene import Scene
from .View import View
from .Model import Model
from .Canvas import Canvas


class DlMarkupApplication:
    """Application class to connect all parts together."""

    def __init__(self, *args):
        """Initialize application.

        :param args: command line arguments
        """
        self.app = QtWidgets.QApplication([])
        self._setTranslation()
        scene = Scene(0, 0, 512, 512)
        undo_redo = UndoRedo(scene)
        canvas = Canvas(scene, undo_redo)
        canvas.setViewport(QtWidgets.QOpenGLWidget())
        model = Model(canvas. args)
        self.view = View(model, canvas)

    def _setTranslation(self):
        """Set up translation to locale language."""
        locale_str = locale.getlocale(locale.LC_MESSAGES)[0]
        self.translator = QTranslator()
        print("Locale:", locale_str)
        self.translator.load(f"dl_markup.{locale_str}")
        if not self.app.installTranslator(self.translator):
            print("Can not install translation")

    def run(self) -> int:
        """Run application."""
        self.view.show()
        return self.app.exec_()
