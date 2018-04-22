from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import uuid

class Node(QtWidgets.QGraphicsItem):
    contextName = None
    def __init__(self, **kwargs):
        #Harvest kwargs and then pass on
        self.name = kwargs.pop("name",None)
        self.uuid = kwargs.pop("uuid",None)
        super(Node, self).__init__(**kwargs)

        self.fillColor = QtGui.QColor("#B1C9C5")
        self.highlightColor = QtGui.QColor("#454545")

        #Configuration.
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setCursor(QtCore.Qt.SizeAllCursor)

        self.setAcceptHoverEvents(True)
        self.setAcceptTouchEvents(True)
        self.setAcceptDrops(True)

    def mouseMoveEvent(self, event):
        '''A placeholder overload'''
        super(Node, self).mouseMoveEvent(event)

    def highlight(self, toggle):
        if toggle:
            self._oldFillColor = self.fillColor
            self.fillColor = self.highlightColor
        else:
            self.fillColor = self._oldFillColor

    def hoverEnterEvent(self, event):
        self.highlight(True)
        super(Node, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.highlight(False)
        super(Node, self).hoverLeaveEvent(event)

    def destroy(self):
        '''Remove Node'''
        scene = self.scene()
        scene.removeItem(self)
        del self

class Box(Node):
    contextName = "Box"
    def __init__(self, **kwargs):
        #Harvest kwargs and then pass on
        self.x = kwargs.pop("x1",0.0)
        self.y = kwargs.pop("y1",0.0)
        self.z = kwargs.pop("z1",0.0)
        self.l = kwargs.pop("l",5.0)
        self.w = kwargs.pop("w",5.0)
        self.h = kwargs.pop("h",5.0)
        self.roundness = kwargs.pop("roundness",5.0)
        super(Box, self).__init__(**kwargs)
        #You can now change inherited things
        self.fillColor = QtGui.QColor("#676d39")

    def boundingRect(self):
        '''Return the bounding box of the item'''
        return QtCore.QRectF(self.x,self.y,self.l,self.w)

    def paint(self, painter, option, widget):
        """Draw the Node's container rectangle."""
        painter.setBrush(QtGui.QBrush(self.fillColor))
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))

        bbox = self.boundingRect()
        painter.drawRoundedRect(self.x,self.y,self.l,self.w,self.roundness,self.roundness)


class Pipe(Node):
    contextName = "Pipe"
    def __init__(self, **kwargs):
        #Harvest kwargs and then pass on
        self.x1 = kwargs.pop("x1",0.0)
        self.y1 = kwargs.pop("y1",0.0)
        self.z1 = kwargs.pop("z1",0.0)
        self.x2 = kwargs.pop("x2",0.0)
        self.y2 = kwargs.pop("y2",0.0)
        self.z2 = kwargs.pop("z2",0.0)
        self.outerRadius = kwargs.pop("outerRadius",5)
        self.innerRadius = kwargs.pop("innerRadius",5)
        super(Pipe, self).__init__(**kwargs)
        #You can now change inherited things
        self.fillColor = QtGui.QColor("#778ab5")


    def boundingRect(self):
        '''Return the bounding box of the item'''
        return QtCore.QRectF(self.x1,self.y1,self.x2-self.x1,self.y2-self.y1)
        
    def paint(self, painter, option, widget):
        """Draw the Node's container rectangle."""
        painter.setBrush(QtGui.QBrush(self.fillColor))
        painter.setPen(QtGui.QPen(self.fillColor,self.outerRadius))


        bbox = self.boundingRect()
        painter.drawEllipse(QtCore.QPointF(self.x1,self.y1),self.outerRadius+1,self.outerRadius+1)    
        painter.drawLine(self.x1,self.y1,self.x2,self.y2)
        painter.drawEllipse(QtCore.QPointF(self.x2,self.y2),self.outerRadius+1,self.outerRadius+1)        
