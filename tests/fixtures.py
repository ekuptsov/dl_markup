from PyQt5 import QtWidgets
import pytest

from dl_markup.undo_redo import UndoRedo
from dl_markup.scene import Scene


@pytest.fixture
def scene_with_undo_redo():
    scene = Scene(0, 0, 512, 512)
    undo_redo = UndoRedo(scene)

    item_1 = QtWidgets.QGraphicsEllipseItem(0, 0, 100, 100)
    item_2 = QtWidgets.QGraphicsLineItem(15, 20, 45, 120)
    undo_redo.insert_in_undo_redo_add(item_1)
    undo_redo.insert_in_undo_redo_add(item_2)

    return ((item_1, item_2), scene, undo_redo)
