from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import header as h

class BuilderScene(QtWidgets.QGraphicsScene):
    def __init__(self,parent=None):
        super(BuilderScene, self).__init__(parent=parent)
        self.setSceneRect(QtCore.QRectF(0.0, 0.0, 2000., 2000.))
        self.setBackgroundBrush(QtGui.QColor("#4C5454"))
        self.testItem()

    def testItem(self):
        item1 = h.Header("TEST")
        self.addItem(item1)

    def mousePressEvent(self, event):
        super(BuilderScene, self).mousePressEvent(event)
        if not event.isAccepted():
            #Add new item with shift + right mouse
            if (event.button() == QtCore.Qt.RightButton and
                event.modifiers() == QtCore.Qt.ShiftModifier):
                event.accept()
                idNumb = len(self.items())
                item = h.Header("WC"+str(idNumb))
                pt = event.scenePos()
                item.setPos(pt.x(),pt.y())
                self.addItem(item)
            else:
                event.ignore()
