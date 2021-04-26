from PyQt5 import QtWidgets
from pytestqt import qtbot

from dl_markup.undo_redo import UndoRedo
from dl_markup.scene import Scene


def test_undo_redo(qtbot):
    scene = Scene(0, 0, 512, 512)
    undo_redo = UndoRedo(scene)

    item_1 = QtWidgets.QGraphicsEllipseItem(0, 0, 100, 100)
    item_2 = QtWidgets.QGraphicsLineItem(15, 20, 45, 120)
    undo_redo.insert_in_undo_redo_add(item_1)
    undo_redo.insert_in_undo_redo_add(item_2)

    undo_redo.undo(2)
    undo_redo.undo(1)

    undo_redo.redo(2)
    undo_redo.redo(1)

    undo_redo.undo(2)

    undo_redo.redo(1)
    undo_redo.redo(1)

    assert len(scene.items()) == 2
    assert item_1 in scene.items()
    assert item_2 in scene.items()
