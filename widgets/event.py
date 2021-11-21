

from PyQt5 import QtWidgets as qtw

from PyQt5 import QtCore as qtc

from  date_validate import DateValidator
class Event(qtw.QFrame):
    buttonClicked = qtc.pyqtSignal()

    def __init__(self,
                 name='dd',
                 start='00:00',
                 finish='00:00'):
        '''MainWindow constructor'''
        super().__init__()
        self.setStyleSheet(''' QPushButton{
        background-color: #E4BAD4;
        border-radius: 8px;
        color: #FFFFFF;
        font-size: 12pt;
    }
        QPushButton::hover{
     border-color: #E4BAD4;
        color:  #F6DFEB;
        border-width: 1px;
        border-style:solid;
    }
   QWidget{
        background-color: #F6DFEB;
    }
    QLineEdit {
    background-color: #F8EDED;
    color:#000000;
    border: none;
    border-radius:8px;
    }
    QLineEdit::hover {
    border: 1px solid  #E4BAD4;
    }''')
        self.setWindowTitle('Add a child')
        layout = qtw.QHBoxLayout()
        layout.setSpacing(5)
        self.setLayout(layout)
        self.setWindowFlags(self.windowFlags() | qtc.Qt.Tool)
        self.name = qtw.QLineEdit(self, placeholderText='Type here...')
        self.name.setFixedWidth(175)
        self.line1 = qtw.QLineEdit(start)
        self.line1.setValidator(DateValidator())
        self.line1.setFixedWidth(50)
        tire = qtw.QLabel('—')
        tire.setFixedWidth(10)
        self.line2 = qtw.QLineEdit(finish)
        self.line2.setValidator(DateValidator())
        self.line2.setFixedWidth(50)
        apply = qtw.QPushButton('Apply')
        apply.clicked.connect(self.buttonClicked.emit)
        layout.addWidget(self.name, alignment=qtc.Qt.AlignLeft)
        layout.addStretch(0)
        layout.addWidget(self.line1, alignment=qtc.Qt.AlignRight)
        layout.addWidget(tire, alignment=qtc.Qt.AlignRight)
        layout.addWidget(self.line2, alignment=qtc.Qt.AlignRight)
        layout.addWidget(apply, alignment=qtc.Qt.AlignRight)
        self.show()