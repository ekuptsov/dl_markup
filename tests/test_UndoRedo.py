from fixtures import scene_with_undo_redo


def test_undo_1(qapp, scene_with_undo_redo):
    (item_1, _), scene, undo_redo = scene_with_undo_redo

    undo_redo.undo(1)

    assert len(scene.items()) == 1
    assert item_1 in scene.items()


def test_undo_2(qapp, scene_with_undo_redo):
    _, scene, undo_redo = scene_with_undo_redo

    undo_redo.undo(2)

    assert len(scene.items()) == 0


def test_redo_1(qapp, scene_with_undo_redo):
    (item_1, _), scene, undo_redo = scene_with_undo_redo

    undo_redo.undo(2)

    undo_redo.redo(1)

    assert len(scene.items()) == 1
    assert item_1 in scene.items()


def test_redo_2(qapp, scene_with_undo_redo):
    (item_1, item_2), scene, undo_redo = scene_with_undo_redo

    undo_redo.undo(2)

    undo_redo.redo(2)

    assert len(scene.items()) == 2
    assert item_1 in scene.items()
    assert item_2 in scene.items()
