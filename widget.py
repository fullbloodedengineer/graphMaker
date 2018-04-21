from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from viewer import GridView
import component as c
import os

class BuilderSpace(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(BuilderSpace, self).__init__(parent=parent)
        self.scene = QtWidgets.QGraphicsScene()
        self.view = GridView()
        self.view.setScene(self.scene)

        #Configuration
        self.view.setRenderHint(QtGui.QPainter.Antialiasing)
        self.view.setViewportUpdateMode(
            QtWidgets.QGraphicsView.FullViewportUpdate)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)
        self.MODIFIER = None

        self.currentNode = c.Pipe

    def clearScene(self):
        '''Make a new scene and leave the old one for garbage collection'''
        self.scene = QtWidgets.QGraphicsScene()
        self.view.setScene(self.scene)

    def _createItem(self,pos):
        _gitem = self.currentNode()
        _gitem.setPos(pos)
        self.scene.addItem(_gitem)

    def keyPressEvent(self, event):
        '''Hot key type events will all be grabbed by widget'''      
        self.MODIFIER = event.key()
        self.setCursor(QtCore.Qt.CrossCursor)
        super(BuilderSpace, self).keyPressEvent(event)

    def keyReleaseEvent(self, event):
        """Trigger a redraw of Edges to update their color."""
        self.MODIFIER = None
        self.setCursor(QtCore.Qt.ArrowCursor)
        super(BuilderSpace, self).keyPressEvent(event)

    def contextMenuEvent(self, event):
        """Show a menu to create registered Nodes."""
        menu = QtWidgets.QMenu(self)
        openFileAction = menu.addAction("Open File")
        openFileAction.triggered.connect(self._loadFile)

        toggleGrid = menu.addAction("Toggle BG Grid")
        toggleGrid.triggered.connect(self._gridLines)

        drawOrigin = menu.addAction("Toggle Origin Marker")
        drawOrigin.triggered.connect(self._drawOrigin)
                
        menu.exec_(event.globalPos())
        super(BuilderSpace, self).contextMenuEvent(event)


    def _loadFile(self):
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName()
        if filePath:
            print filePath

    def _gridLines(self):
        self.view.gridOn = not self.view.gridOn
        self.scene.update()

    def _drawOrigin(self):
        self.view.origin = not self.view.origin
        self.scene.update()