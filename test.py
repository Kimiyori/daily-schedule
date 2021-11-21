import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import json
import os
import datetime
STYLESHEET = '''QTreeView::branch:has-siblings:!adjoins-item {
    border-image: url(vline.png) 0;
}

QTreeView::branch:has-siblings:adjoins-item {
    border-image: url(branch-more.png) 0;
}

QTreeView::branch:!has-children:!has-siblings:adjoins-item {
    border-image: url(branch-end.png) 0;
}

QTreeView::branch:has-children:!has-siblings:closed,
QTreeView::branch:closed:has-children:has-siblings {
        border-image: none;
        image: url(branch-closed.png);
}

QTreeView::branch:open:has-children:!has-siblings,
QTreeView::branch:open:has-children:has-siblings  {
        border-image: none;
        image: url(branch-open.png);
}
QTreeView::item { padding: 10px }
QTreeView::item {margin-bottom:7%; }'''

class Event(qtw.QFrame):

    buttonClicked = qtc.pyqtSignal()

    def __init__(self,
                 name='dd',
                 start='1',
                 finish='1'):
        '''MainWindow constructor'''
        super().__init__()

        layout=qtw.QHBoxLayout()
        layout.setSpacing(5)
        self.setLayout(layout)

        self.line = qtw.QLineEdit(name)
        self.line.setFixedWidth(175)
        self.line1 = qtw.QLineEdit(start)
        self.line1.setFixedWidth(50)
        tire=qtw.QLabel('—')
        tire.setFixedWidth(10)
        self.line2 = qtw.QLineEdit(finish)
        self.line2.setFixedWidth(50)
        apply=qtw.QPushButton('Apply')
        apply.clicked.connect(self.buttonClicked.emit)
        layout.addWidget(self.line,alignment=qtc.Qt.AlignLeft)
        layout.addStretch(0)
        layout.addWidget(self.line1,alignment=qtc.Qt.AlignRight)
        layout.addWidget(tire, alignment=qtc.Qt.AlignRight)
        layout.addWidget(self.line2, alignment=qtc.Qt.AlignRight)
        layout.addWidget(apply, alignment=qtc.Qt.AlignRight)
        self.show()

class MyBar(qtw.QWidget):

    def __init__(self, parent):
        super(MyBar, self).__init__()
        self.parent = parent
        self.layout = qtw.QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.title = qtw.QLabel("My Own Bar")

        btn_size = 25

        self.btn_close = qtw.QPushButton("x")
        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_close.setFixedSize(btn_size,btn_size)
        self.btn_close.setStyleSheet("background-color: red;")

        self.btn_min = qtw.QPushButton("-")
        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_min.setFixedSize(btn_size, btn_size)
        self.btn_min.setStyleSheet("background-color: gray;")

        self.btn_max = qtw.QPushButton("+")
        self.btn_max.clicked.connect(self.btn_max_clicked)
        self.btn_max.setFixedSize(btn_size, btn_size)
        self.btn_max.setStyleSheet("background-color: gray;")

        self.title.setFixedHeight(35)
        self.title.setAlignment(qtc.Qt.AlignCenter)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.btn_min)
        self.layout.addWidget(self.btn_max)
        self.layout.addWidget(self.btn_close)

        self.title.setStyleSheet("""
            background-color: black;
            color: white;
        """)
        self.setLayout(self.layout)

        self.start = qtc.QPoint(0, 0)
        self.pressing = False

    def resizeEvent(self, QResizeEvent):
        super(MyBar, self).resizeEvent(QResizeEvent)
        self.title.setFixedWidth(self.parent.width())

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end-self.start
            self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
                                self.mapToGlobal(self.movement).y(),
                                self.parent.width(),
                                self.parent.height())
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False


    def btn_close_clicked(self):
        self.parent.close()

    def btn_max_clicked(self):
        self.parent.showMaximized()

    def btn_min_clicked(self):
        self.parent.showMinimized()


class te(qtw.QTreeWidget):

    buttonClicked = qtc.pyqtSignal()

    def __init__(self, parent):
        super().__init__()


        self.setDragDropMode(qtw.QAbstractItemView.InternalMove)
        self.setSelectionMode(qtw.QAbstractItemView.ExtendedSelection)


    def dropEvent(self, event):

        return super(te,self).dropEvent(event)
class MainWindow(qtw.QMainWindow):

    def __init__(self):
        '''MainWindow constructor'''
        super().__init__()
        layout = qtw.QVBoxLayout()
        # and populate it upper widget
        layout.addWidget(MyBar(self))
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setMinimumSize(300,400)
        da=qtw.QWidget()
        layout.addWidget(da)
        da_layout = qtw.QHBoxLayout()
        da_layout.setContentsMargins(0, 0, 0, 0)
        da_layout.setSpacing(0)
        da.setLayout(da_layout)
        username = os.getlogin()
        label_name = qtw.QLabel(f'Hello {username}')
        da_layout.addWidget(label_name, alignment=qtc.Qt.AlignLeft)
        label_name1 = qtw.QLabel(f'Choose day of the week')
        da_layout.addWidget(label_name1, alignment=qtc.Qt.AlignRight)
        self.day = qtw.QComboBox(
            self,
            editable=False,
            insertPolicy=qtw.QComboBox.InsertAtTop
        )
        week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for x in week:
            self.day.addItem(x, 1)
        self.day.setCurrentIndex(datetime.datetime.today().weekday())
        self.day.currentIndexChanged.connect(self.write)
        da_layout.addWidget(self.day, alignment=qtc.Qt.AlignRight)


        self.setWindowFlags(qtc.Qt.FramelessWindowHint)
        self.tree = te(self)

        self.tree.setContextMenuPolicy(qtc.Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.openMenu)

        self.tree.setColumnCount(3)
        self.tree.setHeaderLabels(["Name", "Start", 'Finish',''])
        self.write()
        self.scroll = qtw.QScrollArea(self)
        self.scroll.setFixedSize(400, 400)
        self.scroll.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.tree)
        self.tree.expandAll()
        self.tree.setStyleSheet(STYLESHEET)
        self.tree.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)
        self.tree.itemChanged.connect(self.rewrite)
        #self.get_all_items(self.tree)
        header = self.tree.header()
        header.setSectionResizeMode(qtw.QHeaderView.ResizeToContents)
        #header.setStretchLastSection(False)
        header.setSectionResizeMode(0, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(1, qtw.QHeaderView.Stretch)
        layout.addWidget(self.scroll)

        entry_layout=qtw.QHBoxLayout()
        entry=qtw.QWidget()
        entry.setLayout(entry_layout)
        self.line = qtw.QLineEdit('')
        self.line.setFixedWidth(175)
        self.line1 = qtw.QLineEdit('')
        self.line1.setFixedWidth(50)
        tire = qtw.QLabel('—')
        tire.setFixedWidth(10)
        self.line2 = qtw.QLineEdit('')
        self.line2.setFixedWidth(50)
        entry_layout.addWidget(self.line, alignment=qtc.Qt.AlignLeft)
        entry_layout.addStretch(0)
        entry_layout.addWidget(self.line1, alignment=qtc.Qt.AlignRight)
        entry_layout.addWidget(tire, alignment=qtc.Qt.AlignRight)
        entry_layout.addWidget(self.line2, alignment=qtc.Qt.AlignRight)
        layout.addWidget(entry)

        set_days = qtw.QPushButton('Add Event')
        set_days.clicked.connect(self.add_new)
        layout.addWidget(set_days)
        mainWidget = qtw.QWidget()
        mainWidget.setLayout(layout)
        self.setCentralWidget(mainWidget)
        self.show()

    def openMenu(self, position):
            indexes = self.sender().selectedIndexes()
            mdlIdx = self.tree.indexAt(position)
            if not mdlIdx.isValid():
                return
            if len(indexes) > 0:
                level = 0
                index = indexes[0]
                while index.parent().isValid():
                    index = index.parent()
                    level += 1
            else:
                level = 0
            right_click_menu = qtw.QMenu()
            act_add = right_click_menu.addAction(self.tr("Add Child Item"))
            act_add.triggered.connect(self.add_child)
            act_del = right_click_menu.addAction(self.tr("Delete Item"))
            act_del.triggered.connect(self.de)
            right_click_menu.exec_(self.sender().viewport().mapToGlobal(position))

    def chil(self):
        item = qtw.QTreeWidgetItem([self.ev.line.text(), self.ev.line1.text(), self.ev.line2.text()])
        item.setFlags(item.flags() | qtc.Qt.ItemIsEditable)
        bb = qtw.QPushButton('')
        bb.setIcon(qtg.QIcon('F:\Programs\python\pyqt\daily schedule\delete_outline_icon_148544.png'))
        bb.clicked.connect(lambda: self.de(item))
        bb.setFixedSize(30, 25)
        currNode = self.tree.currentItem()
        currNode.addChild(item)
        self.tree.setItemWidget(item, 3, bb)
        self.tree.expandAll()
        self.ev.close()
        self.rewrite()


    def add_child(self):
        self.ev=Event()
        self.ev.buttonClicked.connect(self.chil)

    def add_new(self):
        item = qtw.QTreeWidgetItem([self.line.text(), self.line1.text(), self.line2.text()])
        item.setFlags(item.flags() | qtc.Qt.ItemIsEditable)
        bb = qtw.QPushButton('')
        bb.setIcon(qtg.QIcon('F:\Programs\python\pyqt\daily schedule\delete_outline_icon_148544.png'))
        bb.clicked.connect(lambda: self.de(item))
        bb.setFixedSize(30, 25)
        self.tree.addTopLevelItem(item)
        self.tree.setItemWidget(item, 3, bb)
        self.tree.expandAll()
        self.rewrite()

    def get_subtree_nodes(self,tree_widget_item):
        """Returns all QTreeWidgetItems in the subtree rooted at the given node."""
        nodes = {tree_widget_item.text(0):{'start':tree_widget_item.text(1),
                                           'finish':tree_widget_item.text(2),
                                           'somes':{}}}
        for i in range(tree_widget_item.childCount()):
            if tree_widget_item.child(i).childCount()!=0:
                nodes[tree_widget_item.text(0)]['somes'].update(self.get_subtree_nodes(tree_widget_item.child(i)))
            else:
                nodes[tree_widget_item.text(0)]['somes'].update(
                    {tree_widget_item.child(i).text(0):{
                        'start': tree_widget_item.child(i).text(1),
                        'finish': tree_widget_item.child(i).text(2),
                    'somes':{}}})
        return nodes

    def get_all_items(self,tree_widget):
        """Returns all QTreeWidgetItems in the given QTreeWidget."""
        all_items = {}
        for i in range(tree_widget.topLevelItemCount()):
            top_item = tree_widget.topLevelItem(i)
            all_items.update(self.get_subtree_nodes(top_item))
        #print(json.dumps(all_items,indent=2,ensure_ascii=False))
        return all_items

    def de(self,child):
        try:
            # Попробуйте удалить дочерний узел (через его родительский узел вызовите функцию removeChild для удаления)
            currNode = self.tree.currentItem()
            parent1 = currNode.parent()
            parent1.removeChild(currNode)
            self.rewrite()
        except Exception:
            # Удаляем корневой узел при возникновении исключения
            try:
                rootIndex = self.tree.indexOfTopLevelItem(currNode)
                self.tree.takeTopLevelItem(rootIndex)
                self.rewrite()
            except Exception:
                print(Exception)

    def repe(self,main, chil):
        item = main
        values = chil
        for keys, value in values['somes'].items():
            name = keys
            start = value['start']
            finish = value['finish']
            bb = qtw.QPushButton('')
            bb.setFixedSize(30, 25)
            bb.setIcon(qtg.QIcon('F:\Programs\python\pyqt\daily schedule\delete_outline_icon_148544.png'))
            child = qtw.QTreeWidgetItem([name, start, finish])
            bb.clicked.connect(lambda: self.de(child))
            child.setFlags(item.flags() | qtc.Qt.ItemIsEditable)
            item.addChild(child)
            self.tree.setItemWidget(child, 3, bb)
            if 'somes' in value:
                    return self.repe(child, value)

    def write(self):
        self.tree.clear()
        with open('F:\Programs\python\pyqt\daily schedule\package.json', encoding='utf8') as f:
            token = json.load(f)
            day=self.day.currentText()
            for key, values in token[day].items():
                try:
                    item = qtw.QTreeWidgetItem([key,values['start'],values['finish']])
                    self.repe(item,values)
                except Exception as e:
                    print(e)

                item.setFlags(item.flags() | qtc.Qt.ItemIsEditable)
                bb = qtw.QPushButton('')
                bb.setIcon(qtg.QIcon('F:\Programs\python\pyqt\daily schedule\delete_outline_icon_148544.png'))
                bb.clicked.connect(lambda: self.de(item))
                bb.setFixedSize(30,25)
                self.tree.addTopLevelItem(item)
                self.tree.setItemWidget(item, 3, bb)
        self.tree.expandAll()


    def rewrite(self):
        with open('package.json',encoding='utf8') as f:
            token = json.load(f)
            tr = self.get_all_items(self.tree)
            day=self.day.currentText()
            token[day]=tr
            with open('package.json', 'w',encoding='utf8') as outfile:
                json.dump(token, outfile,indent=2,ensure_ascii=False)

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
