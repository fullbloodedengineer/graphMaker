import json

from PyQt5 import QtGui
from PyQt5 import QtCore

def readFileContent(filePath):
    with open(filePath) as f:
        return f.read()

def toJson(serialized):
    return json.dumps(serialized, encoding="utf-8", indent=4)

def fromJson(jsonString):
    return json.loads(jsonString, encoding="utf-8")

def getTextSize(text, painter=None):
    if not painter:
        metrics = QtGui.QFontMetrics(QtGui.QFont())
    else:
        metrics = painter.fontMetrics()
    size = metrics.size(QtCore.Qt.TextSingleLine, text)
    return size
