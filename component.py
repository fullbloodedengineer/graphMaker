from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import uuid

class Node(QtWidgets.QGraphicsItem):
    contextName = None
    def __init__(self, **kwargs):
        super(Node, self).__init__()
        self.name = kwargs.get("name",None)
        self.uuid = kwargs.get("uuid",None)
        self.fillColor = self.baseColor = QtGui.QColor("#778ab5")
        self.highlightColor = QtGui.QColor("#454545")

        #Configuration.
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable,True)
        self.setCursor(QtCore.Qt.SizeAllCursor)
        self.setAcceptHoverEvents(True)
        self.setAcceptTouchEvents(True)
        self.setAcceptDrops(True)

        #self.setContextMenuPolicy(QtWidgets.Qt.CustomContextMenu)
        #self.connect(self,SIGNAL('customContextMenuRequested(QPoint)'), self.contextMenu)

    def contextMenuEvent(self, event):
        #import time
        """Show a menu to create registered Nodes."""
        menu = QtWidgets.QMenu()
        openFileAction = menu.addAction("Test")
        #openFileAction.triggered.connect(time.time)
        menu.exec_(event.screenPos())
        super(Node, self).contextMenuEvent(event)

    def mouseClickEvent(self, event):
        '''A placeholder overload'''
        print "Click..."
        if self.window().Alt_Key == QtCore.Qt.Key_Alt:       
            print "Do something special"
        super(Node, self).mouseClickEvent(event)

    def highlight(self, toggle):
        #if not self.isSelected():
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
        super(Box, self).__init__(**kwargs)
        #Harvest kwargs and then pass on
        x,y,z = kwargs.get("point",[0.,0.,0.])
        self.size = kwargs.get("size",[1.,1.,1.])
        self.roundness = kwargs.get("roundness",5.0)
        #You can now change inherited things
        self.fillColor = QtGui.QColor("#676d39")
        self.setPos(x,y)

    def boundingRect(self):
        '''Return the bounding box of the item'''
        return QtCore.QRectF(QtCore.QPointF(),QtCore.QSizeF(self.size[0],self.size[1]))

    def paint(self, painter, option, widget):
        """Draw the Node's container rectangle."""
        _color = self.fillColor
        _colorShadow = self.fillColor.darker(240)
        sbox = QtCore.QRectF(QtCore.QPointF(2,3),QtCore.QSizeF(self.size[0],self.size[1]))
        bbox = self.boundingRect()
        painter.setOpacity(self.scene().opacity)
        if self.scene().shadows:
            painter.setBrush(QtGui.QBrush(_colorShadow))
            painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
            painter.drawRoundedRect(sbox ,self.roundness,self.roundness)

        painter.setBrush(QtGui.QBrush(_color))
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        painter.drawRoundedRect(bbox ,self.roundness,self.roundness)


class ControlPoint(Node):
    contextName = "Pipe"
    def __init__(self,x,y,z, **kwargs):
        super(ControlPoint, self).__init__(**kwargs)
        self.setPos(x,y)

    def boundingRect(self):
        '''Return the bounding box of the item'''
        _cp = QtCore.QPointF()
        _size = QtCore.QSizeF(self.parentItem().outerRadius+1,self.parentItem().outerRadius+1)
        return QtCore.QRectF(_cp,_size)

    def paint(self, painter, option, widget):
        pass

class Pipe(Node):
    contextName = "Pipe"
    def __init__(self, **kwargs):
        super(Pipe, self).__init__()
        self.outerRadius = kwargs.get("outerRadius",5)
        self.innerRadius = kwargs.get("innerRadius",5)
        self.fillColor = self.baseColor = QtGui.QColor("#778ab5")
        for point in kwargs.get("points",5):
            x,y,z = point
            _pItem = ControlPoint(x,y,z)
            _pItem.setParentItem(self)

    def boundingRect(self):
        return self.childrenBoundingRect()

    def shape(self):
        controlPoints = self.childItems()
        path = QtGui.QPainterPath()
        for i in range(len(controlPoints)-1):
            x1 = controlPoints[i].pos().x()
            y1 = controlPoints[i].pos().y()
            x2 = controlPoints[i+1].pos().x()
            y2 = controlPoints[i+1].pos().y()
            path.moveTo(x1,y1)               
            path.lineTo(x2,y2)
        return path
  
    def paint(self, painter, option, widget):
        """Draw the Node's container rectangle."""
        if len(self.childItems()) > 1:
            _color = self.fillColor
            _colorShadow = self.fillColor.darker(240)
            _size = self.outerRadius+1
            controlPoints = self.childItems()

            path = QtGui.QPainterPath()
            #Draw drop shadow
            if self.scene().shadows:
                pathShadow = QtGui.QPainterPath()
                painter.setBrush(QtGui.QBrush(_colorShadow))
                painter.setPen(QtGui.QPen(_colorShadow,self.outerRadius))
                painter.setOpacity(self.scene().opacity)
                for i in range(len(controlPoints)-1):
                    x1 = controlPoints[i].pos().x()+2
                    y1 = controlPoints[i].pos().y()+3
                    x2 = controlPoints[i+1].pos().x()+2
                    y2 = controlPoints[i+1].pos().y()+3

                    painter.drawEllipse(QtCore.QPointF(x1,y1),_size,_size)
                    painter.drawEllipse(QtCore.QPointF(x2,y2),_size,_size)
                    #painter.drawLine(x1,y1,x2,y2)
                    pathShadow.moveTo(x1,y1)               
                    pathShadow.lineTo(x2,y2)
            painter.drawPath(pathShadow)
                    
            #Draw object
            painter.setBrush(QtGui.QBrush(_color))
            painter.setPen(QtGui.QPen(_color,self.outerRadius))
            for i in range(len(controlPoints)-1):
                x1 = controlPoints[i].pos().x()
                y1 = controlPoints[i].pos().y()
                x2 = controlPoints[i+1].pos().x()
                y2 = controlPoints[i+1].pos().y()

                painter.drawEllipse(QtCore.QPointF(x1,y1),_size,_size)
                painter.drawEllipse(QtCore.QPointF(x2,y2),_size,_size)
            painter.drawPath(self.shape())
