from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QAbstractButton
from PyQt5.QtCore import QCoreApplication

from typing import List

from .Scene import Scene
from .UndoRedo import UndoRedo
from .BrushTool import Brush
from .PolygonTool import Polygon


class Canvas(QtWidgets.QGraphicsView):
    """A class capable of user interaction with scene.

    Inherits QtWidgets.QGraphicsView, so it can be placed in layout.
    Store scene, undo_redo module and available tool.
    """

    def __init__(self, scene: Scene, undo_redo: UndoRedo):
        """Create a new canvas.

        :param scene: scene object for drawing
        :param undo_redo: an object for storing history
        """
        super().__init__(scene)
        self.scene = scene
        self.undo_redo = undo_redo
        # green is default color
        self.tool = Brush(self, QtGui.QColor(0, 255, 0))
        self.setCursor(self.tool.cursor())

        self.zoom = 1.
        self.zoom_factor = 1.04

    def mouseMoveEvent(self, e):
        """Propagate event to sons and call tool handler.

        :param e: event object
        """
        super().mouseMoveEvent(e)
        self.tool.mouseMoveEvent(e)

    def mousePressEvent(self, e):
        """Propagate event to sons and call tool handler.

        :param e: event object
        """
        super().mousePressEvent(e)
        self.tool.mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        """Propagate event to sons and call tool handler.

        :param e: event object
        """
        super().mouseReleaseEvent(e)
        self.tool.mouseReleaseEvent(e)

    def keyPressEvent(self, e):
        """Change tool size by pressing '+' and '-' buttons.

        Implemented only for brush tool.
        :param e: event object
        """
        super().keyPressEvent(e)
        self.tool.keyPressEvent(e)

    def changeTool(self, buttons: List[QAbstractButton]):
        """Switch between markup tools.

        Press sender button and rise another.
        Only support Brush and Polygon.
        :param buttons: list of Brush and Polygon buttons
        """
        sender = self.sender()
        tool_color = self.tool.color
        brush_text = QCoreApplication.translate('View', 'Brush')
        polygon_text = QCoreApplication.translate('View', 'Polygon')
        # switch tool by button text
        if sender.text() == brush_text:
            if isinstance(self.tool, Polygon):
                # clear canvas from intermidiate verticies and edges
                self.tool.clear()
            self.tool = Brush(self, tool_color)
        elif sender.text() == polygon_text:
            self.tool = Polygon(self, tool_color)
        assert len(buttons) == 2, "Support exactly 2 tools"
        # small hint to choose another button
        prev_button = buttons[sender == buttons[0]]
        # and rise it
        prev_button.setChecked(False)

    def changeToolColor(self, color: str):
        """Change tool color by their string description.

        Call QColor.colorNames() staticmethod to figure out
        valid strings that QColor knows about.
        :param color: new color of tool
        """
        self.tool.color = QtGui.QColor(color)

    def _zoom(self, angle_delta: QtCore.QPointF):
        # set new anchor
        old_anchor = self.transformationAnchor()
        new_anchor = QtWidgets.QGraphicsView.ViewportAnchor.AnchorViewCenter
        self.setTransformationAnchor(new_anchor)

        # zoom
        zoom_factor = self.zoom_factor
        if angle_delta.y() < 0:
            zoom_factor = 1 / self.zoom_factor
        self.zoom *= zoom_factor
        self.scale(zoom_factor, zoom_factor)
        # dont forget update cursor
        self.setCursor(self.tool.cursor())
        # reset old anchor
        self.setTransformationAnchor(old_anchor)

    def wheelEvent(self, e):
        if e.modifiers() & QtCore.Qt.ControlModifier:
            self._zoom(e.angleDelta())
        else:
            super().wheelEvent(e)

    def clear(self):
        """Clear scene and history."""
        self.scene.clear()
        self.undo_redo.clear()

    def updateBackgroundImage(self, img_path: str):
        """Update background image with clearing current segmentation.

        :param img_path: path to new background image
        """
        self.clear()
        self.scene.img = QtGui.QPixmap(img_path)
