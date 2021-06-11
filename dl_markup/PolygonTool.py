from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QBrush, QColor, QGradient

from typing import Union

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .Canvas import Canvas


class VertexItem(QtWidgets.QGraphicsRectItem):
    """Represent future coordinates of vertecies in PolygonItem.

    Support interactive moving (hold mouse),
    incident egdes redrawing and outgoing egde mouse following.
    """

    def __init__(
            self,
            incoming_edge: QtWidgets.QGraphicsLineItem,
            side: float,
            pen: Union[QPen, QColor, Qt.GlobalColor, QGradient] = None,
            brush: Union[QBrush, QColor, Qt.GlobalColor, QGradient] = None,
            parent: QtWidgets.QGraphicsRectItem = None):
        """Represent vertex of Polygon tool.

        :param incoming_egde:
        :param side: side lenght of drawing rectangle representing the vertex
        :param pen: pen that used in RectItem and LineItem
        :param brush: brush that used in RectItem
        :param parent: parent layout object
        """
        rect = QtCore.QRectF(0, 0, side, side)
        self.side = side
        self.halfSide = side / 2
        super().__init__(rect, parent)
        self.incoming_edge = incoming_edge

        self.outgoing_edge = QtWidgets.QGraphicsLineItem(
            0, 0, 1, 1, parent=self)
        self.outgoing_edge.setPos(self.rect().center())
        self.setBrush(brush)
        self.setPen(pen)
        self.outgoing_edge.setPen(pen)

        # make vertex support iteractive movement
        self.setAcceptHoverEvents(True)
        movable_flag = QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable
        self.setFlag(movable_flag)
        self.leaved = False

    def hoverEnterEvent(self, e):
        if not self.leaved:
            return
        rect = QtCore.QRectF(0, 0, 2 * self.side, 2 * self.side)
        self.setRect(rect)
        self.moveBy(-self.halfSide, -self.halfSide)
        self.outgoing_edge.moveBy(self.halfSide, self.halfSide)

    def hoverLeaveEvent(self, e):
        if not self.leaved:
            self.leaved = True
            return
        self.moveBy(self.halfSide, self.halfSide)
        self.outgoing_edge.moveBy(-self.halfSide, -self.halfSide)
        rect = QtCore.QRectF(0, 0, self.side, self.side)
        self.setRect(rect)
        self.leaved = True

    def mouseMoveEvent(self, e):
        """When vertex is moved, incident edges are changed too."""
        old_vertex_center = self.scenePos() + self.rect().center()
        super().mouseMoveEvent(e)
        new_vertex_center = self.scenePos() + self.rect().center()

        # every vertex except the first one have incoming edge
        if self.incoming_edge is not None:
            line_pos = self.incoming_edge.scenePos()
            mouse = new_vertex_center - line_pos
            self.incoming_edge.setLine(0, 0, mouse.x(), mouse.y())

        # outgoing edge binds to vertex
        # so it lenght increases by the
        # opposite of vertex motion vector
        p2 = self.outgoing_edge.line().p2()
        p2 += old_vertex_center - new_vertex_center
        self.outgoing_edge.setLine(0, 0, p2.x(), p2.y())


class Polygon:
    """Tool that draw polygon using VertexItems marked by user.

    Hold all marked verticies in list. If user click on first
    vertex, tool will draw QGraphicsPolygonItem and clear canvas from
    intermidiate vertecies and lines. User can undo existing
    QGraphicsPolygonItems.
    """

    def __init__(self, canvas: 'Canvas', color: Union[QColor, Qt.GlobalColor]):
        """Initialize Polygon.

        :param canvas: сanvas object for drawing
        :param color: color of polygon
        """
        self.canvas = canvas
        self.color = color
        self.vertex_side = 6.
        self.verticies = []
        self.canvas.setCursor(self.cursor())

    def mousePressEvent(self, e):
        """Add new VertexItem on canvas.

        If user click on first vertex, tool draw Polygon.
        """
        scene_point = self.canvas.mapToScene(e.pos())

        collidingItems = self.canvas.scene.items(scene_point)
        collidingVertecies = [
            item
            for item in collidingItems
            if isinstance(item, QtWidgets.QGraphicsRectItem)]

        if collidingVertecies:
            init_vertex = self.verticies[0]
            # user click on first vertex
            if init_vertex in collidingItems:
                self.drawPolygon()
                self.clear()
            return

        incoming_edge = \
            self.verticies[-1].outgoing_edge if self.verticies else None

        vertex = VertexItem(
            incoming_edge,
            self.vertex_side,
            pen=self.color,
            brush=self.color,
            parent=self.canvas.scene.background_item)
        vertex.setPos(scene_point - vertex.rect().center())
        self.verticies.append(vertex)

    def mouseMoveEvent(self, e):
        """Draw a line that connect previous vertex and current mouse pos."""
        scene_point = self.canvas.mapToScene(e.pos())
        if self.verticies:
            tracking_line = self.verticies[-1].outgoing_edge
            line_pos = tracking_line.scenePos()
            mouse = scene_point - line_pos
            tracking_line.setLine(0, 0, mouse.x(), mouse.y())

    def mouseReleaseEvent(self, e):
        """Skip event."""
        pass

    def keyPressEvent(self, e):
        """Skip event."""
        pass

    def cursor(self):
        """Crosscursor increase markup precision."""
        return Qt.CrossCursor

    def clear(self):
        """Accurately free resources and erase intermidiate steps."""
        for vertex in self.verticies:
            # vertex removed with outgoing edge
            self.canvas.scene.removeItem(vertex)
        self.verticies.clear()

    def drawPolygon(self):
        """Draw Polygon based on VerexItems centers."""
        points = QtGui.QPolygonF(
            vertex.scenePos() + vertex.rect().center()
            for vertex in self.verticies)
        polygon = QtWidgets.QGraphicsPolygonItem(
            points,
            self.canvas.scene.background_item)
        polygon.setBrush(self.color)
        polygon.setPen(self.color)
        # undo-redo only polygon, not verticies
        self.canvas.undo_redo.insert_in_undo_redo_add(polygon)
