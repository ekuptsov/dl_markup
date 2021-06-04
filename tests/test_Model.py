from PyQt5.QtWidgets import QFileDialog

from dl_markup.Model import Model
from dl_markup.Canvas import Canvas

from fixtures import scene_with_undo_redo


def test_select_input_directory_1(
        qapp,
        scene_with_undo_redo,
        monkeypatch):
    _, scene, undo_redo = scene_with_undo_redo

    canvas = Canvas(scene, undo_redo)
    model = Model(canvas, './', './')

    monkeypatch.setattr(
        QFileDialog,
        'getExistingDirectory',
        lambda *args: './resources'
    )
    model.selectInputDirectory()

    assert 'Lenna.png' in model.listModel.items
    assert model.inputDirectory.text() == './resources'


def test_select_input_directory_2(
        qapp,
        scene_with_undo_redo,
        monkeypatch):
    _, scene, undo_redo = scene_with_undo_redo

    canvas = Canvas(scene, undo_redo)
    model = Model(canvas, './', './')

    init_items = model.listModel.items
    init_text = model.inputDirectory.text()

    monkeypatch.setattr(
        QFileDialog,
        'getExistingDirectory',
        lambda *args: ''
    )
    model.selectInputDirectory()

    assert model.listModel.items == init_items
    assert model.inputDirectory.text() == init_text


def test_select_output_directory(
        qapp,
        scene_with_undo_redo,
        monkeypatch):
    _, scene, undo_redo = scene_with_undo_redo

    canvas = Canvas(scene, undo_redo)
    model = Model(canvas, './', './')

    monkeypatch.setattr(
        QFileDialog,
        'getExistingDirectory',
        lambda *args: './resources'
    )
    model.selectOutputDirectory()

    assert model.outputDirectory.text() == './resources'
