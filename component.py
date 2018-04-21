from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import uuid

class Node(QtWidgets.QGraphicsItem):

    def __init__(self, **kwargs):
        super(Node, self).__init__(**kwargs)

        #Provide a uid
        self.uuid = str(uuid.uuid4())
        self.fillColor = QtGui.QColor("#B1C9C5")
        #self.x = 0
        #self.y = 0
        #self.w = 60
        #self.h = 20

        #Configuration.
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setCursor(QtCore.Qt.SizeAllCursor)

        self.setAcceptHoverEvents(True)
        self.setAcceptTouchEvents(True)
        self.setAcceptDrops(True)
    """
    def boundingRect(self):
        '''Return the bounding box of the item'''
        return QtCore.QRectF(self.x,self.y,self.w,self.h)

    def paint(self, painter, option, widget):
        '''Draw the Node's container rectangle.'''
        painter.setBrush(QtGui.QBrush(self.fillColor))
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))

        bbox = self.boundingRect()
        painter.drawRect(self.x,self.y,self.w,self.h)
    """
    def mouseMoveEvent(self, event):
        '''A placeholder overload'''
        super(Node, self).mouseMoveEvent(event)

    def destroy(self):
        '''Remove Node'''
        scene = self.scene()
        scene.removeItem(self)
        del self

class Box(Node):
    def __init__(self, **kwargs):
        super(Pipe, self).__init__(**kwargs)
        self.roundness = 0
        self.x = 0
        self.y = 0
        self.w = 60
        self.h = 20

    def paint(self, painter, option, widget):
        """Draw the Node's container rectangle."""
        painter.setBrush(QtGui.QBrush(self.fillColor))
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))

        bbox = self.boundingRect()
        painter.drawRect(self.x,self.y,self.w,self.h,self.roundness,self.roundness)


class Pipe(Node):
    def __init__(self, **kwargs):
        super(Pipe, self).__init__(**kwargs)
        self.x1 = 0
        self.y1 = 0
        self.x2 = 100
        self.y2 = 0
        
    def paint(self, painter, option, widget):
        """Draw the Node's container rectangle."""
        painter.setBrush(QtGui.QBrush(self.fillColor))
        painter.setPen(QtGui.QPen(self.fillColor))

        bbox = self.boundingRect()
        painter.drawLine(self.x1,self.y1,self.x2,self.y2)    