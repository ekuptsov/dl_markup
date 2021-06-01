from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QPixmap, QPainter

from .CylinderItem import CylinderItem


class Brush:

    def __init__(self, canvas, color=QtGui.QColor(0, 255, 0)):
        self.canvas = canvas
        self.color = color
        self.last_x, self.last_y = None, None
        self.mouse_pressed = False
        self.radius = 20

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = min(value, 63)
        # redraw cursor
        self.canvas.setCursor(self.cursor())

    @radius.deleter
    def radius(self):
        del self._radius

    def cursor(self):
        return self._CircleCursor()

    def _CircleCursor(self):
        """Draw a circle cursor of the same size as brush."""
        pixmap_size = 128
        pixmap = QPixmap(pixmap_size, pixmap_size)
        pixmap.fill(Qt.GlobalColor.transparent)

        # draw circle on pixmap
        painter = QPainter()
        painter.begin(pixmap)
        if hasattr(self.canvas, 'zoom'):
            diameter = self.radius * self.canvas.zoom * 2
        else:
            diameter = self.radius * 2
        left = (pixmap_size - diameter) // 2
        top = (pixmap_size - diameter) // 2
        # draw bbox in (left, top) with size (diameter, diameter)
        painter.drawEllipse(left, top, diameter, diameter)
        painter.end()
        return QCursor(pixmap)

    def mouseMoveEvent(self, e):
        """Draw cylinder between previous and current mouse positions.

        :param e: event object
        """
        canvas = self.canvas
        if canvas.scene.img_item is None:
            return
        if not self.mouse_pressed:
            return

        scene_point = canvas.mapToScene(e.pos())

        # cursor has moved outside of the scene
        if scene_point.x() < 0 or \
                scene_point.y() < 0 or \
                scene_point.x() > canvas.scene.width() - 1 or \
                scene_point.y() > canvas.scene.height() - 1:
            self.last_x, self.last_y = None, None
            return

        if self.last_x is None:  # First event.
            self.last_x = scene_point.x()
            self.last_y = scene_point.y()
            return  # Ignore the first time.

        cylinder = CylinderItem(
            QtCore.QPointF(self.last_x, self.last_y),
            QtCore.QPointF(scene_point.x(), scene_point.y()),
            self.radius,
            pen=QtGui.QPen(self.color),
            brush=QtGui.QBrush(self.color),
            parent=canvas.scene.background_item,
        )
        canvas.undo_redo.insert_in_undo_redo_add(cylinder)

        # Update the origin for next time.
        self.last_x = scene_point.x()
        self.last_y = scene_point.y()

    def mousePressEvent(self, e):
        if e.button() == Qt.RightButton:
            self.color = QtGui.QColor(0, 0, 0)
        scene_point = self.canvas.mapToScene(e.pos())
        self.last_x = scene_point.x()
        self.last_y = scene_point.y()
        self.mouse_pressed = True

    def mouseReleaseEvent(self, e):
        """Clear mouse position info.

        :param e: event object
        """
        self.last_x = None
        self.last_y = None
        self.mouse_pressed = False

    def keyPressEvent(self, e):
        """Change brush size by pressing '+' and '-' buttons.

        :param e: event object
        """
        if e.key() == Qt.Key_Plus or e.key() == Qt.Key_Equal:
            self.radius = self.radius + 1
        elif e.key() == Qt.Key_Minus:
            self.radius = max(1, self.radius - 1)
        else:
            return
        # self.setCursor(self._CircleCursor())
        print("New brush size:", self.radius)


class Vertex(QtWidgets.QGraphicsRectItem):

    def __init__(self, incoming_edge, outgoing_edge, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.incoming_edge = incoming_edge
        self.outgoing_edge = outgoing_edge
        # make vertex support iteractive movement
        self.setAcceptHoverEvents(True)
        movable_flag = QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable
        self.setFlag(movable_flag)

    def mouseMoveEvent(self, e):
        """When vertex is moved, incident edges are changed too."""
        super().mouseMoveEvent(e)
        scene_point = self.mapToScene(e.pos())

        if self.incoming_edge is not None:
            line_pos = self.incoming_edge.scenePos()
            mouse = scene_point - line_pos
            self.incoming_edge.setLine(0, 0, mouse.x(), mouse.y())

        edge_pos = self.outgoing_edge.scenePos()
        edge_len = self.outgoing_edge.line().p2()
        # outgoing edge starts at mouse pointer, ends as before
        self.outgoing_edge.setPos(scene_point)
        edge_len += edge_pos - scene_point
        self.outgoing_edge.setLine(0, 0, edge_len.x(), edge_len.y())


class Polygon:

    def __init__(self, canvas, color=QtGui.QColor(0, 255, 0)):
        self.canvas = canvas
        self.color = color
        self.vertex_side = QtCore.QPointF(6., 6.)
        self.verticies = []
        self.line = None

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
            if isinstance(item, QtWidgets.QGraphicsRectItem)
        ]

        if collidingVertecies:
            init_vertex = self.verticies[0]
            # user click on first vertex
            if init_vertex in collidingItems:
                self.drawPolygon()
                self.clear()
            return

        endline = self.line  # (!)

        self.line = QtWidgets.QGraphicsLineItem(
            0, 0, 1, 1,
            parent=self.canvas.scene.background_item)
        self.line.setPos(scene_point)
        self.line.setPen(QtGui.QPen(self.color))

        # (!) ugly constuctor
        vertex = Vertex(
            endline,
            self.line,
            QtCore.QRectF(QtCore.QPointF(0., 0.), self.vertex_side),
            parent=self.canvas.scene.background_item)
        vertex.setPos(scene_point - self.vertex_side / 2)
        vertex.setBrush(QtGui.QBrush(self.color))
        self.verticies.append(vertex)

    def mouseMoveEvent(self, e):
        """Draw a line that connect previous vertex and current mouse pos."""
        scene_point = self.canvas.mapToScene(e.pos())
        if self.line:
            line_pos = self.line.scenePos()
            mouse = scene_point - line_pos
            self.line.setLine(0, 0, mouse.x(), mouse.y())

    def mouseReleaseEvent(self, e):
        pass

    def keyPressEvent(self, e):
        pass

    def cursor(self):
        return Qt.CrossCursor

    def clear(self):
        # n_vertecies == n_edges
        for vertex in self.verticies:
            self.canvas.scene.removeItem(vertex)
            self.canvas.scene.removeItem(vertex.outgoing_edge)  # (!)
        self.verticies.clear()
        self.line = None

    def drawPolygon(self):
        points = QtGui.QPolygonF(
            vertex.scenePos() + self.vertex_side / 2
            for vertex in self.verticies)
        polygon = QtWidgets.QGraphicsPolygonItem(
            points,
            self.canvas.scene.background_item)
        polygon.setBrush(self.color)
        polygon.setPen(self.color)
