
from PyQt5 import QtWidgets as qtw

from  .date_validate import DateValidator
class TreeWidgetDelegate(qtw.QStyledItemDelegate):
    def __init__(self, parent=None):
        qtw.QStyledItemDelegate.__init__(self, parent=parent)

    def createEditor(self, parent, option, index=1):
        editor = qtw.QLineEdit(parent)

        editor.setValidator(DateValidator())
        return editor