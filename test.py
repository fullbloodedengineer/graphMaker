from PyQt5 import QtGui
from PyQt5 import QtWidgets
import widget as w

def test():
    app = QtWidgets.QApplication([])
    app.setApplicationName("graphMaker")
    graph = w.BuilderSpace()
    graph.setGeometry(100, 100, 800, 600)
    graph.show()
    app.exec_()

if __name__ == '__main__':
    test()
