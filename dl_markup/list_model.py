from PyQt5 import QtCore
from PyQt5.QtCore import Qt


class ListModel(QtCore.QAbstractListModel):
    def __init__(self, *args, items=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = items or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.items[index.row()]

    def rowCount(self, index):
        return len(self.items)

    def setItems(self, items):
        self.items = items
        self.layoutChanged.emit()
