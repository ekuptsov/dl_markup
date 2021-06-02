from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QBrush, QColor, QGradient

from typing import Union


class VertexItem(QtWidgets.QGraphicsRectItem):

    def __init__(
            self,
            incoming_edge,
            side: float,
            pen: Union[QPen, QColor, Qt.GlobalColor, QGradient] = None,
            brush: Union[QBrush, QColor, Qt.GlobalColor, QGradient] = None,
            parent=None):
        """Represent vertex of PolygonTool."""
        rect = QtCore.QRectF(0, 0, side, side)
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

        p2 = self.outgoing_edge.line().p2()
        p2 += old_vertex_center - new_vertex_center
        self.outgoing_edge.setLine(0, 0, p2.x(), p2.y())


class Polygon:

    def __init__(self, canvas, color: Union[QColor, Qt.GlobalColor]):
        self.canvas = canvas
        self.color = color
        self.vertex_side = 6.
        self.verticies = []

    def mousePressEvent(self, e):
        """
        Click on empty space -- create new vertex and associate it with line
        Click on existing vertex -- select vertex to movement

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
        pass

    def keyPressEvent(self, e):
        pass

    def cursor(self):
        return Qt.CrossCursor

    def clear(self):
        for vertex in self.verticies:
            # vertex removed with outgoing edge
            self.canvas.scene.removeItem(vertex)
        self.verticies.clear()

    def drawPolygon(self):
        points = QtGui.QPolygonF(
            vertex.scenePos() + vertex.rect().center()
            for vertex in self.verticies)
        polygon = QtWidgets.QGraphicsPolygonItem(
            points,
            self.canvas.scene.background_item)
        polygon.setBrush(self.color)
        polygon.setPen(self.color)
        self.canvas.undo_redo.insert_in_undo_redo_add(polygon)
