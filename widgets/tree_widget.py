

from PyQt5 import QtWidgets as qtw
import typing
from PyQt5 import QtCore as qtc



class MyTreeWidget(qtw.QTreeWidget):


    def keyPressEvent(self, event):
        if (event.key() == qtc.Qt.Key_Escape and
            event.modifiers() == qtc.Qt.NoModifier):
            self.selectionModel().clear()
        else:
            super(MyTreeWidget, self).keyPressEvent(event)

    def mousePressEvent(self, event):
        if not self.indexAt(event.pos()).isValid():
            self.selectionModel().clear()
        super(MyTreeWidget, self).mousePressEvent(event)
  