import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5 import QtMultimedia as qtm
import json
import os
import datetime
import time
import pymorphy2
import enchant
from style import STYLESHEET
from widgets import check_days,date_validate,dial,event,my_bar,toaster,tree_widget,value_validate,tree_delegate



class MainWindow(qtw.QMainWindow):

    def __init__(self):
        '''MainWindow constructor'''
        super().__init__()
        self.setObjectName('MainWindow')
        main_layout = qtw.QVBoxLayout()
        # and populate it upper widget
        main_layout.addWidget(my_bar.MyBar(self))
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setMinimumSize(300, 400)
        main_widget = qtw.QWidget()
        main_horisontal_layout = qtw.QHBoxLayout()
        main_widget.setLayout(main_horisontal_layout)
        main_layout.addWidget(main_widget)
        self.setStyleSheet(STYLESHEET)
        left_widget = qtw.QWidget()
        left_layout = qtw.QVBoxLayout()
        left_widget.setLayout(left_layout)
        main_horisontal_layout.addWidget(left_widget)

        upper_left_widget = qtw.QWidget()
        left_layout.addWidget(upper_left_widget)
        upper_left_layout = qtw.QHBoxLayout()
        upper_left_layout.setContentsMargins(0, 0, 0, 0)
        upper_left_layout.setSpacing(0)
        upper_left_widget.setLayout(upper_left_layout)
        username = os.getlogin()
        label_name = qtw.QLabel(f'Hello {username}')
        upper_left_layout.addWidget(label_name, alignment=qtc.Qt.AlignLeft)
        choose_label = qtw.QLabel(f'Choose day of the week')
        upper_left_layout.addWidget(choose_label, alignment=qtc.Qt.AlignRight)
        self.pick_day = qtw.QComboBox(
            self,
            editable=False,
            insertPolicy=qtw.QComboBox.InsertAtTop
        )
        week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for x in week:
            self.pick_day.addItem(x, 1)
        self.pick_day.setCurrentIndex(datetime.datetime.today().weekday())
        self.pick_day.currentIndexChanged.connect(self.write)
        upper_left_layout.addWidget(self.pick_day, alignment=qtc.Qt.AlignRight)

        self.setWindowFlags(qtc.Qt.FramelessWindowHint)
        self.tree = tree_widget.MyTreeWidget()
    
        delegate = tree_delegate.TreeWidgetDelegate()

        self.tree.setItemDelegateForColumn(1, delegate)
        self.tree.setItemDelegateForColumn(2, delegate)

        self.tree.setContextMenuPolicy(qtc.Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.openMenu)

        self.tree.setColumnCount(3)
        self.tree.setHeaderLabels(["Name", "Start", 'Finish'])
        self.write()
        self.scroll = qtw.QScrollArea(self)
        self.scroll.setFixedSize(400, 300)
        self.scroll.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.tree)
        self.tree.expandAll()
        #self.tree.setStyleSheet(STYLESHEET)
        #self.tree.setSelectionMode(qtw.QAbstractItemView.ExtendedSelection)
        self.tree.setSelectionMode(qtw.QAbstractItemView.SingleSelection)
        self.tree.setDragEnabled(True)
        self.tree.setAcceptDrops(True)
        self.tree.setDropIndicatorShown(True)
        self.tree.setDragDropMode(qtw.QAbstractItemView.InternalMove)
        self.tree.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)
        self.tree.itemChanged.connect(self.sorting)
        header = self.tree.header()
        header.setSectionResizeMode(qtw.QHeaderView.ResizeToContents)
        # header.setStretchLastSection(False)
        header.setSectionResizeMode(0, qtw.QHeaderView.Stretch)
        header.setSectionResizeMode(1, qtw.QHeaderView.Stretch)

        right_widget = qtw.QWidget()
        right_layout = qtw.QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(15)
        right_widget.setLayout(right_layout)
        self.dial = dial.ValueDial(minimum=0, maximum=60, pageStep=5, singleStep=5, wrapping=1)
        self.dial.valueChanged.connect(self.dialchan)
        right_layout.addWidget(self.dial, alignment=qtc.Qt.AlignTop)
        minutes_value = qtw.QLabel('Minutes: ')
        self.value = qtw.QLineEdit('0')
        self.value.setValidator(value_validate.ValueValidator())
        self.move_time_button = qtw.QPushButton('Move timer')
        self.move_time_button.setObjectName('main_button')
        self.move_time_button.clicked.connect(self.move_min)
        form_box = qtw.QFormLayout()
        form_box.addRow(minutes_value, self.value)
        self.start_notifications = qtw.QPushButton('Start notifications')
        self.start_notifications.setObjectName('main_button')
        self.start_notifications.clicked.connect(self.notifications)

        pause_layout = qtw.QHBoxLayout()
        self.pause = qtw.QPushButton('Pause')
        self.pause.setObjectName('main_button')
        self.pause.clicked.connect(self.pause_func)
        pause_layout.addWidget(self.pause)

        self.resume = qtw.QPushButton('Resume')
        self.resume.setObjectName('main_button')
        self.resume.clicked.connect(self.resume_func)
        pause_layout.addWidget(self.resume)

        self.correct_to_cur_time = qtw.QPushButton('Correct to current time')
        self.correct_to_cur_time.setObjectName('main_button')
        self.correct_to_cur_time.clicked.connect(self.correct)
        self.save = qtw.QPushButton('Save')
        self.save.setObjectName('main_button')
        self.save.clicked.connect(lambda:self.rewrite(self.pick_day.currentText()))

        copy_layout=qtw.QHBoxLayout()
        self.copy = qtw.QPushButton('Copy')
        self.copy.setObjectName('main_button')
        self.copy.clicked.connect(self.copy_schedule)
        self.pick_day2 = check_days.CheckableComboBox()
        self.pick_day2.addItems(week)
        copy_layout.addWidget(self.copy)
        copy_layout.addWidget(self.pick_day2)

        right_layout.addLayout(form_box)
        right_layout.addWidget(self.move_time_button)
        right_layout.addWidget(self.correct_to_cur_time)
        right_layout.addWidget(self.start_notifications)
        right_layout.addLayout(pause_layout)
        right_layout.addWidget(self.save)
        right_layout.addLayout(copy_layout)
        right_layout.addStretch()

        main_horisontal_layout.addWidget(right_widget)
        left_layout.addWidget(self.scroll)

        entry_layout = qtw.QHBoxLayout()
        entry = qtw.QWidget()
        entry.setLayout(entry_layout)
        self.name = qtw.QLineEdit(self, placeholderText='Text event...')
        self.name.setFixedWidth(175)
        self.start_time = qtw.QLineEdit('00:00')
        self.start_time.setValidator(date_validate.DateValidator())
        self.start_time.setFixedWidth(50)
        tire = qtw.QLabel('—')
        tire.setFixedWidth(10)
        self.finish_time = qtw.QLineEdit('00:00')
        self.finish_time.setValidator(date_validate.DateValidator())
        self.finish_time.setFixedWidth(50)
        entry_layout.addWidget(self.name, alignment=qtc.Qt.AlignLeft)
        entry_layout.addStretch(0)
        entry_layout.addWidget(self.start_time, alignment=qtc.Qt.AlignRight)
        entry_layout.addWidget(tire, alignment=qtc.Qt.AlignRight)
        entry_layout.addWidget(self.finish_time, alignment=qtc.Qt.AlignRight)
        left_layout.addWidget(entry)
        self.format = 'HH:mm'
        set_days = qtw.QPushButton('Add Event')
        set_days.setObjectName('main_button')
        set_days.clicked.connect(self.add_new)
        left_layout.addWidget(set_days)
        mainWidget = qtw.QWidget()
        mainWidget.setLayout(main_layout)
        self.setCentralWidget(mainWidget)
        self.setWindowFlags(self.windowFlags() | qtc.Qt.FramelessWindowHint |
                            qtc.Qt.BypassWindowManagerHint | qtc.Qt.SplashScreen)
        self.show()

    def pause_func(self):
        try:
            self.remain=self.timer.remainingTime()
            print(self.remain)
            self.timer.stop()
        except Exception as e:
            print(e)

    def resume_func(self):
        try:

            self.set_timer(self.item,self.pos,self.remain)
            print(self.remain)
        except Exception as e:
            print(e)

    def copy_schedule(self):
        list=self.pick_day2.currentData()
        for day in list:
            self.rewrite(day)

    def correct(self):
        def get_subtree_nodes(tree_widget_item, x):
            cur_text = tree_widget_item.text(x)
            new = qtc.QTime.fromString(cur_text, self.format).addSecs(dif).toString(self.format)
            tree_widget_item.setText(x, new)
            if tree_widget_item.childCount() != 0:
                for i in range(tree_widget_item.childCount()):
                    get_subtree_nodes(tree_widget_item.child(i), x)

        current_time = qtc.QTime.currentTime()
        top = self.tree.topLevelItem(0)
        get_first_time = qtc.QTime.fromString(top.text(1), self.format)
        dif = get_first_time.secsTo(current_time)

        for i in range(self.tree.topLevelItemCount()):
            top_item = self.tree.topLevelItem(i)
            for x in range(1, 3):
                get_subtree_nodes(top_item, x)

    def toast(self, name, pos):

        def morph(word):
            d = enchant.Dict("en_US")
            if not d.check(word):
                morph = pymorphy2.MorphAnalyzer()
                butyavka = morph.parse(word)[0]
                gent = butyavka.inflect({'gent'})
                return gent.word.capitalize()
            else:
                return word

        time.sleep(1)
        filename = 'tuturu_1.mp3'
        fullpath = qtc.QDir.current().absoluteFilePath(filename)
        url = qtc.QUrl.fromLocalFile(fullpath)
        content = qtm.QMediaContent(url)
        self.player = qtm.QMediaPlayer()
        self.player.setMedia(content)
        self.player.play()
        if not pos:
            if name.parent():
                #print(f'{name.text(0)} from {morph(name.parent().text(0))} is over!')
                toaster.QToaster.showMessage(self, f'{name.text(0)} from {morph(name.parent().text(0))} is start!')
            else:
                print(name.text(0))
                toaster.QToaster.showMessage(self, f'{name.text(0)} is start!')
        else:
            if name.parent():
                toaster.QToaster.showMessage(self, f'{name.text(0)} from {morph(name.parent().text(0))} is over!')
            else:
                toaster.QToaster.showMessage(self, f'{name.text(0)} is over!')
        self.notifications()

    def set_timer(self,name, pos,remain=0):
        self.timer = qtc.QTimer()
        self.timer.setSingleShot(True)
        if not remain:
            time = self.cur.msecsTo(qtc.QTime.fromString(self.req, self.format))
            print(time / 60000)
            self.timer.setInterval(time)
        else:
            print(remain / 60000)
            self.timer.setInterval(remain)
        self.timer.timeout.connect(lambda: self.toast(name, pos))
        self.timer.start()

    def notifications(self):

        def find_time(parent, req=None, item=None, pos=0):
            def find_child(parent, req=None, item=None, pos=0):
                for id in range(parent.childCount()):
                    if self.cur.secsTo(qtc.QTime.fromString(parent.child(id).text(1), self.format)) > 0:
                        item = parent.child(id)
                        req = item.text(1)
                        pos = 0
                        return item, req, pos
                    elif self.cur.secsTo(qtc.QTime.fromString(parent.child(id).text(2), self.format)) > 0:
                        item = parent.child(id)
                        req = item.text(2)
                        pos = 1
                        if parent.child(id).childCount() != 0:
                            return find_child(parent.child(id), req, item, pos)
                        return item, req, pos
                return item, req, pos

            for id in range(parent.topLevelItemCount()):
                if self.cur.secsTo(qtc.QTime.fromString(parent.topLevelItem(id).text(1), self.format)) > 0:
                    item = parent.topLevelItem(id)
                    req = item.text(1)
                    pos = 0
                    return item, req, pos
                elif self.cur.secsTo(qtc.QTime.fromString(parent.topLevelItem(id).text(2), self.format)) > 0:
                    item = parent.topLevelItem(id)
                    req = item.text(2)
                    pos = 1
                    if parent.topLevelItem(id).childCount() != 0:
                        return find_child(parent.topLevelItem(id), req, item, pos)
                    return item, req, pos
            return item, req, pos

        self.cur = qtc.QTime.currentTime()
        self.item, self.req, self.pos = find_time(self.tree, None, None, 0)

        if self.req is None:
            toaster.QToaster.showMessage(self, 'Day end!!!!')
        else:
            self.set_timer(self.item, self.pos)

    def move_min(self):
        def get_subtree_nodes(tree_widget_item, x):
            cur_text = tree_widget_item.text(x)
            new = qtc.QTime.fromString(cur_text, self.format).addSecs(int(self.value.text()) * 60).toString(self.format)
            tree_widget_item.setText(x, new)
            if tree_widget_item.childCount() != 0:
                for i in range(tree_widget_item.childCount()):
                    get_subtree_nodes(tree_widget_item.child(i), x)

        for i in range(self.tree.topLevelItemCount()):
            top_item = self.tree.topLevelItem(i)
            for x in range(1, 3):
                get_subtree_nodes(top_item, x)

    def sorting(self):
        if self.tree.currentItem():
            if self.tree.currentItem().parent():
                self.tree.currentItem().parent().sortChildren(1, qtc.Qt.AscendingOrder)
                self.tree.currentItem().parent().sortChildren(2, qtc.Qt.AscendingOrder)
            else:
                self.tree.sortByColumn(1, qtc.Qt.AscendingOrder)
                self.tree.sortByColumn(2, qtc.Qt.AscendingOrder)
            # self.rewrite()

    def dialchan(self):
        self.value.setText(str(self.dial.dial.value()))

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
        item = qtw.QTreeWidgetItem([self.ev.name.text(), self.ev.line1.text(), self.ev.line2.text()])
        item.setFlags(item.flags() |qtc.Qt.ItemIsDragEnabled|qtc.Qt.ItemIsDropEnabled| qtc.Qt.ItemIsEditable)
        currNode = self.tree.currentItem()
        currNode.addChild(item)
        self.tree.expandAll()
        self.ev.close()
        self.tree.currentItem().sortChildren(1, qtc.Qt.AscendingOrder)
        # self.rewrite()

    def add_child(self):
        self.ev = event.Event()
        self.ev.buttonClicked.connect(self.chil)

    def add_new(self):
        item = qtw.QTreeWidgetItem([self.name.text(), self.start_time.text(), self.finish_time.text()])
        item.setFlags(item.flags() | qtc.Qt.ItemIsEditable)
        self.tree.addTopLevelItem(item)
        self.tree.expandAll()
        self.tree.sortByColumn(1, qtc.Qt.AscendingOrder)
        # self.rewrite()

    def get_all_items(self, tree_widget):
        def get_subtree_nodes(tree_widget_item):
            """Returns all QTreeWidgetItems in the subtree rooted at the given node."""
            nodes = {tree_widget_item.text(0): {'start': tree_widget_item.text(1),
                                                'finish': tree_widget_item.text(2),
                                                'somes': {}}}
            for i in range(tree_widget_item.childCount()):
                if tree_widget_item.child(i).childCount() != 0:
                    nodes[tree_widget_item.text(0)]['somes'].update(get_subtree_nodes(tree_widget_item.child(i)))
                else:
                    nodes[tree_widget_item.text(0)]['somes'].update(
                        {tree_widget_item.child(i).text(0): {
                            'start': tree_widget_item.child(i).text(1),
                            'finish': tree_widget_item.child(i).text(2),
                            'somes': {}}})
            return nodes

        """Returns all QTreeWidgetItems in the given QTreeWidget."""
        all_items = {}
        for i in range(tree_widget.topLevelItemCount()):
            top_item = tree_widget.topLevelItem(i)
            all_items.update(get_subtree_nodes(top_item))
        # print(json.dumps(all_items,indent=2,ensure_ascii=False))
        return all_items

    def de(self, child):
        try:
            currNode = self.tree.currentItem()
            parent1 = currNode.parent()
            parent1.removeChild(currNode)
            # self.rewrite()
        except Exception:
            try:
                rootIndex = self.tree.indexOfTopLevelItem(currNode)
                self.tree.takeTopLevelItem(rootIndex)
                # self.rewrite()
            except Exception:
                print(Exception)

    def add_time(self, ):
        pass

    def write(self):
        def repe(main, chil):
            if not chil['somes']:
                return
            for keys, value in chil['somes'].items():
                child = qtw.QTreeWidgetItem([keys, value['start'], value['finish']])
                child.setFlags(main.flags()  | qtc.Qt.ItemIsEditable)
                main.addChild(child)
                repe(child, value)

        self.tree.clear()
        with open('package.json', encoding='utf8') as f:
            token = json.load(f)
            day = self.pick_day.currentText()
            for key, values in token[day].items():
                item = qtw.QTreeWidgetItem([key, values['start'], values['finish']])
                repe(item, values)

                item.setFlags(item.flags()  | qtc.Qt.ItemIsEditable)
                self.tree.addTopLevelItem(item)
        self.tree.expandAll()

    def rewrite(self,day=None):
        with open('package.json', encoding='utf8') as f:
            token = json.load(f)
            tr = self.get_all_items(self.tree)
            day = day
            token[day] = tr
            with open('package.json', 'w', encoding='utf8') as outfile:
                json.dump(token, outfile, indent=2, ensure_ascii=False)



if __name__ == '__main__':

    @qtc.pyqtSlot(qtw.QSystemTrayIcon.ActivationReason)
    def slotSystrayActivated(reason):
        if reason == qtw.QSystemTrayIcon.Context:  # right
            pass
        elif reason == qtw.QSystemTrayIcon.MiddleClick:  # middle
            pass
        elif reason == qtw.QSystemTrayIcon.DoubleClick:  # double click
            pass
        elif reason == qtw.QSystemTrayIcon.Trigger:  # left
            if main.isHidden() or main.isMinimized():
                main.setGeometry(main.geometry())
                main.showNormal()
                main.activateWindow()
                main.raise_()
            else:
                main.hide()


    app = qtw.QApplication(sys.argv)

    main = MainWindow()
    # Adding an icon
    icon = qtg.QIcon("pngwing.com.png")

    # Adding item on the menu bar
    tray = qtw.QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)
    tray.activated.connect(slotSystrayActivated)
    menu = qtw.QMenu()
    quit = qtw.QAction("Quit")
    quit.triggered.connect(app.quit)
    menu.addAction(quit)

    tray.setContextMenu(menu)

    sys.exit(app.exec())
   
