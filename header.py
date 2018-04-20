from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

class Header(QtWidgets.QGraphicsItem):
    def __init__(self,text, **kwargs):
        super(Header,self).__init__(**kwargs)
        self.name = text
        self.text = text
        self.w = 80
        self.h = 50
        self.roundness = 5
        self.fillColor = QtGui.QColor("#B1C9C5")
        self.textColor = QtGui.QColor("#FCFC83")
        self.selected = False
        
        #Configuration
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable,True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable,True)
        self.setCursor(QtCore.Qt.SizeAllCursor)
        #self.setFlag(QtWidgets.QGraphicsItem.setMouseTracking,True)

    def boundingRect(self):
        return QtCore.QRectF(self.x(),self.y(),self.w,self.h)

    def getTextSize(self, text, painter=None):
        if not painter:
            metrics = QtGui.QFontMetrics(QtGui.QFont())
        else:
            metrics = painter.fontMetrics()

        return metrics.size(QtCore.Qt.TextSingleLine, text)

    def toggleColor(self):
        if self.fillColor == QtGui.QColor("#B1C9C5"):
            self.fillColor = QtGui.QColor("#000000")
        else:   
            self.fillColor = QtGui.QColor("#B1C9C5")
        self.update()

    def mousePressEvent(self,event):
        self.offset = event.scenePos()

    def mouseMoveEvent(self,event):
        super(Header, self).mouseMoveEvent(event)
        self.setPos( event.pos()-self.offset )
               
    def mouseDoubleClickEvent(self, event):
        super(Header, self).mouseDoubleClickEvent(event)
        event.accept()
        self.toggleColor()

    def paint(self, painter, option, widget):
        # Draw backgroun rectangle
        self.text = "_".join([self.name,str(int(self.x())),str(int(self.y()))])
        bbox = self.boundingRect()
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        painter.setBrush(self.fillColor)
        painter.drawRoundedRect(bbox,self.roundness,self.roundness)
        painter.setPen(QtGui.QPen(self.textColor))
        textSize = self.getTextSize(self.text,painter)
        painter.drawText(self.x()+(self.w - textSize.width()) / 2.,
                            self.y()+(self.h + textSize.height() / 2. ) / 2.,
                            self.text)
