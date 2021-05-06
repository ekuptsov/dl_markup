from abc import ABC, abstractmethod

from PyQt5 import QtWidgets

from .Scene import Scene


class ICommand(ABC):
    """Abstract command."""

    @abstractmethod
    def execute(self):
        """Execute command."""
        pass

    @abstractmethod
    def un_execute(self):
        """Undo command execution."""
        pass


class AddCommand(ICommand):
    """Command adding new item to scene."""

    def __init__(
            self,
            item: QtWidgets.QGraphicsItem,
            scene: Scene):
        """Initialize new command.

        :param item: item to be added to scene
        :param scene: scene to operate with
        """
        self.__item = item
        self.__scene = scene

    def execute(self):
        """Add item to scene."""
        self.__scene.addItem(self.__item)

    def un_execute(self):
        """Remove item from scene."""
        self.__scene.removeItem(self.__item)


class UndoRedo:
    """Class for saving drawing history and performing undo/redo functionality."""

    def __init__(self, scene: Scene):
        """Initialize UndoRedo object.

        :param scene: scene for drawing
        """
        self.__undo_commands = []
        self.__redo_commands = []
        self.__container = scene

    def undo(self, levels: int):
        """Undo last actions.

        :param levels: number of actions to undo
        """
        for _ in range(levels):
            if not self.__undo_commands:
                break
            command = self.__undo_commands.pop()
            command.un_execute()
            self.__redo_commands.append(command)

    def redo(self, levels: int):
        """Redo actions, which were undone.

        :param levels: number of actions to redo
        """
        for _ in range(levels):
            if not self.__redo_commands:
                break
            command = self.__redo_commands.pop()
            command.execute()
            self.__undo_commands.append(command)

    def insert_in_undo_redo(self, command: ICommand):
        """Insert command to history.

        :param command: command to be inserted
        """
        self.__undo_commands.append(command)
        self.__redo_commands.clear()

    def insert_in_undo_redo_add(
            self,
            item: QtWidgets.QGraphicsItem):
        """Insert and execute AddCommand.

        :param item: AddCommand to be executed and added to history
        """
        command = AddCommand(item, self.__container)
        command.execute()
        self.insert_in_undo_redo(command)

    def clear(self):
        """Clear all history."""
        self.__undo_commands.clear()
        self.__redo_commands.clear()
