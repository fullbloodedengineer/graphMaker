from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from viewer import GridView
import helpers
import component as c
import os

class BuilderSpace(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(BuilderSpace, self).__init__(parent=parent)
        self.scene = QtWidgets.QGraphicsScene()
        self.view = GridView()
        self.view.setScene(self.scene)

        #Configuration
        self.view.setRenderHint(QtGui.QPainter.Antialiasing)
        self.view.setViewportUpdateMode(
            QtWidgets.QGraphicsView.FullViewportUpdate)

        centralwidget = QtWidgets.QWidget(self)
        horizontalLayout = QtWidgets.QHBoxLayout()

        centralwidget.setLayout(horizontalLayout)
        dockWidget = QtWidgets.QDockWidget()
        dockWidgetContents = QtWidgets.QWidget()
        verticalLayout = QtWidgets.QVBoxLayout()
        tabWidget = QtWidgets.QTabWidget()
        tab = QtWidgets.QWidget()
        tabWidget.addTab(tab,'Items')
        verticalLayout.addWidget(tabWidget)
        sortClass = QtWidgets.QComboBox()
        verticalLayout.addWidget(sortClass)
        dockWidgetContents.setLayout(verticalLayout)
        dockWidget.setWidget(dockWidgetContents);
        self.addDockWidget(QtCore.Qt.DockWidgetArea(1),dockWidget);
        horizontalLayout.addWidget(self.view)
        self.setCentralWidget(centralwidget)

        self.moveableItems = False
        self.currentNode = None
        self.registeredCls = {"Pipe":c.Pipe,"Box":c.Box}
        self.scene.opacity = 1
        self.scene.shadows = True

    def clearScene(self):
        '''Make a new scene and leave the old one for garbage collection'''
        self.scene = QtWidgets.QGraphicsScene()
        self.view.setScene(self.scene)

    def contextMenuEvent(self, event):
        """Show a menu to create registered Nodes."""
        pos = self.view.getMouseScenePosition()
        menu = QtWidgets.QMenu(self)
        openFileAction = menu.addAction("Open File")
        openFileAction.triggered.connect(self._loadFile)

        clearAllAction = menu.addAction("Clear Everything")
        clearAllAction.triggered.connect(self.clearScene)

        viewMenu = menu.addMenu("View...")
        toggleGrid = viewMenu.addAction("Toggle BG Grid")
        toggleGrid.triggered.connect(self._gridLines)

        drawOrigin = viewMenu.addAction("Toggle Origin Marker")
        drawOrigin.triggered.connect(self._drawOrigin)

        itemLock = viewMenu.addAction("Toggle Object Lock")
        itemLock.triggered.connect(self._itemLock)

        ghostLook = viewMenu.addAction("Toggle Ghosted Look")
        ghostLook.triggered.connect(self._ghostItems)

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
            item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable,self.moveableItems)

    def _loadItem(self,clsName,item):
        clsName = item.get('class',None)
        if self.registeredCls.has_key(clsName):
            cls = self.registeredCls[clsName]
            print "Build a",clsName
            print item
            _gitem = cls(**item)
            self.scene.addItem(_gitem)
            _gitem.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable,self.moveableItems)

    def _ghostItems(self):
        if self.scene.opacity < 1:
            self.scene.opacity = 1
            self.scene.shadows = True
        else:
            self.scene.opacity = 0.6
            self.scene.shadows = False
        self.update()
