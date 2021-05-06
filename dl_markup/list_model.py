from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QModelIndex


class ListModel(QtCore.QAbstractListModel):
    """Store list data according to MVC pattern."""

    def __init__(self, *args, items: list = None, **kwargs):
        """Create a new ListModel object.
        
        :param items: list of initial values
        """
        super().__init__(*args, **kwargs)
        self.items = items or []

    def data(self, index: QModelIndex, role: int):
        """Return stored data by index.

        :param index: index object
        :param role: role from Qt enum values
        """
        if role == Qt.DisplayRole:
            return self.items[index.row()]

    def rowCount(self, index: QModelIndex):
        """Return size of stored list."""
        return len(self.items)

    def setItems(self, items: list):
        """Update data and notify observers.

        :param items: new value for data
        """
        self.items = items
        self.layoutChanged.emit()
