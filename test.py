from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import uic
import widget as w

Ui_Window = uic.loadUiType('graphmaker.ui')[0]

class MyApp(QtWidgets.QMainWindow,Ui_Window):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self,parent)
        self.setupUi(self)
        self.connectAll()

    def connectAll(self):
        self.scene = w.BuilderScene()
        self.builder_graphicsView.setScene(self.scene)

def test():
    app = QtWidgets.QApplication([])
    window = MyApp(None)
    window.show()
    app.exec_()

if __name__ == '__main__':
    test()
