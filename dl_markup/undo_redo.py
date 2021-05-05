from abc import ABC, abstractmethod

from PyQt5 import QtWidgets

from .scene import Scene


class ICommand(ABC):

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def un_execute(self):
        pass


class AddCommand(ICommand):

    def __init__(
            self,
            item: QtWidgets.QGraphicsItem,
            scene: Scene):
        self.__item = item
        self.__scene = scene

    def execute(self):
        self.__scene.addItem(self.__item)

    def un_execute(self):
        self.__scene.removeItem(self.__item)


class UndoRedo:

    def __init__(self, scene: Scene):
        self.__undo_commands = []
        self.__redo_commands = []
        self.__container = scene

    def undo(self, levels: int):
        for _ in range(levels):
            if not self.__undo_commands:
                break
            command = self.__undo_commands.pop()
            command.un_execute()
            self.__redo_commands.append(command)

    def redo(self, levels: int):
        for _ in range(levels):
            if not self.__redo_commands:
                break
            command = self.__redo_commands.pop()
            command.execute()
            self.__undo_commands.append(command)

    def insert_in_undo_redo(self, command: ICommand):
        self.__undo_commands.append(command)
        self.__redo_commands.clear()

    def insert_in_undo_redo_add(
            self,
            item: QtWidgets.QGraphicsItem):
        command = AddCommand(item, self.__container)
        command.execute()
        self.insert_in_undo_redo(command)

    def clear(self):
        self.__undo_commands.clear()
        self.__redo_commands.clear()