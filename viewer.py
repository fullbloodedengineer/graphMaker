from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets


CURRENT_ZOOM = 1.0
ALTERNATE_MODE_KEY = QtCore.Qt.Key_Alt

class GridView(QtWidgets.QGraphicsView):
    """A view with a grid in its background and zoom effects."""

    def __init__(self, *args, **kwargs):
        super(GridView, self).__init__(*args, **kwargs)

        #Set a BG color and some grid lines to keep perspective
        self.fillColor = QtGui.QColor("#4C5454")
        self.lineColor = QtGui.QColor(self.fillColor).darker(120)
        self.originColor = QtGui.QColor("#FCFC83")

        self.xStep = 10
        self.yStep = 10

        self.panningMult = 2.0 * CURRENT_ZOOM
        self.panning = False
        self.zoomStep = 1.1
        self.prevPos = QtCore.QPoint(0,0)
        # Since we implement custom panning, we don't need the scrollbars.
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        
        self.gridOn = True
        self.origin = True

    def drawBackground(self, painter, rect):
        painter.setBrush(QtGui.QBrush(self.fillColor))
        painter.drawRect(rect)

        if self.gridOn:
            painter.setPen(QtGui.QPen(self.lineColor))
            top = rect.top()
            bottom = rect.bottom()
            left = rect.left()
            right = rect.right()

            lines = []
            currentXPos = left
            while currentXPos <= right:
                line = QtCore.QLineF(currentXPos, top, currentXPos, bottom)
                lines.append(line)
                currentXPos += self.xStep

            currentYPos = top
            while currentYPos <= bottom:
                line = QtCore.QLineF(left, currentYPos, right, currentYPos)
                lines.append(line)
                currentYPos += self.yStep
            painter.drawLines(lines)

        if self.origin:
            painter.setPen(QtGui.QPen(self.originColor))
            painter.drawEllipse(0,0,5,5)

    def wheelEvent(self, event):
        positive = event.angleDelta().y() >= 0
        zoom = self.zoomStep if positive else 1.0 / self.zoomStep
        #Scale the current view transformation by (sx, sy)
        self.scale(zoom, zoom)
        #make the zoom level global so it can be used by everything
        #transform.m11() Returns the horizontal scaling factor.
        global CURRENT_ZOOM
        CURRENT_ZOOM = self.transform().m11()

    def getMouseScenePosition(self):
        return self.mapToScene(self.mapFromGlobal(QtGui.QCursor.pos()))
 
    def mousePressEvent(self, event):
        '''Initiate custom panning using middle mouse button.
            Right button reserved for context menu'''
        if event.button() == QtCore.Qt.MiddleButton:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self.panning = True
            self.prevPos = event.pos()
            self.setCursor(QtCore.Qt.SizeAllCursor)
        elif event.button() == QtCore.Qt.LeftButton:
                self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        super(GridView, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.panning:
            delta = (self.mapToScene(event.pos()) * self.panningMult -
                     self.mapToScene(self.prevPos) * self.panningMult) * -1.0
            center = QtCore.QPoint(self.viewport().width() / 2 + delta.x(),
                                   self.viewport().height() / 2 + delta.y())
            newCenter = self.mapToScene(center)
            self.centerOn(newCenter)
            self.prevPos = event.pos()
            return
        super(GridView, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.panning:
            self.panning = False
            self.setCursor(QtCore.Qt.ArrowCursor)
        super(GridView, self).mouseReleaseEvent(event)
