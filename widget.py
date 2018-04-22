from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from viewer import GridView
import helpers
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

        self.moveableItems = False
        self.currentNode = None
        self.registeredCls = {"Pipe":c.Pipe,"Box":c.Box}

    def clearScene(self):
        '''Make a new scene and leave the old one for garbage collection'''
        self.scene = QtWidgets.QGraphicsScene()
        self.view.setScene(self.scene)

    def _createItem(self,cls,pos):
        pass

    def contextMenuEvent(self, event):
        """Show a menu to create registered Nodes."""
        pos = self.view.getMouseScenePosition()
        menu = QtWidgets.QMenu(self)
        openFileAction = menu.addAction("Open File")
        openFileAction.triggered.connect(self._loadFile)

        viewMenu = menu.addMenu("View...")
        toggleGrid = viewMenu.addAction("Toggle BG Grid")
        toggleGrid.triggered.connect(self._gridLines)

        drawOrigin = viewMenu.addAction("Toggle Origin Marker")
        drawOrigin.triggered.connect(self._drawOrigin)

        itemLock = viewMenu.addAction("Toggle Object Lock")
        itemLock.triggered.connect(self._itemLock)

        #nodeMenu = menu.addMenu("Nodes...")
        #for cls in  self.registeredCls:
        #    _action = nodeMenu.addAction(cls.contextName)
        #    _action.triggered.connect(lambda x: self._createItem(cls,pos))                

        menu.exec_(event.globalPos())
        super(BuilderSpace, self).contextMenuEvent(event)

    def _changeCurrentNodeType(self,cls):
        print "Changing Build type to:",cls.contextName
        self.currentNode = cls
               
    def _loadFile(self):
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName()
        if filePath:
            text = helpers.readFileContent(filePath)
            sceneData = helpers.fromJson(text)
            for node in sceneData:
                for item in sceneData[node]:
                    self._loadItem(node,item) 

    def _gridLines(self):
        self.view.gridOn = not self.view.gridOn
        self.scene.update()

    def _drawOrigin(self):
        self.view.origin = not self.view.origin
        self.scene.update()

    def _itemLock(self):
        self.moveableItems = not self.moveableItems
        targetType = c.Node().type()
        for item in self.scene.items():
            if item.type() == targetType:
                item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable,self.moveableItems)

    def _loadItem(self,clsName,item):
        #clsName = item.pop('class',None)
        if self.registeredCls.has_key(clsName):
            cls = self.registeredCls[clsName]
            print "Build a",clsName
            _gitem = cls(**item)
            _gitem.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable,self.moveableItems)
            self.scene.addItem(_gitem)


