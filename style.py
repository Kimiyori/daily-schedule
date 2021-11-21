STYLESHEET = '''QTreeView::branch:has-siblings:!adjoins-item {
    border-image: url(vline.png) 0;
}

QTreeView::branch:has-siblings:adjoins-item {
    border-image: url(branch-more.png) 0;
}

QTreeView::branch:!has-children:!has-siblings:adjoins-item {
    border-image: url(branch-end.png) 0;
}
QTreeView::item:hover{background-color:#E4BAD4;;}
QTreeView::branch:has-children:!has-siblings:closed,
QTreeView::branch:closed:has-children:has-siblings {
        border-image: none;
        image: url(branch-closed.png);
}
QTreeView::item:selected { background-color:#E4BAD4; }
QTreeView::branch:open:has-children:!has-siblings,
QTreeView::branch:open:has-children:has-siblings  {
        border-image: none;
        image: url(branch-open.png);
}
QTreeView::item { padding: 10px }
QTreeView::item {margin-bottom:7%; }
 QPushButton#main_button{
        background-color: #E4BAD4;
        border-radius: 8px;
        color: #FFFFFF;
        font-size: 10pt;
    }
        QPushButton#main_button::hover{
     border-color: #E4BAD4;
        color:  #F6DFEB;
        border-width: 1px;
        border-style:solid;
    }
   QWidget#MainWindow{
        background-color: #F6DFEB;
    }
     QComboBox {
        color: #000000;
        background-color:  #F6DFEB;
        border: 1px solid #E4BAD4;
    }
QTreeWidget{
        background-color: #F8EDED;   
        border: 0px;
        background-image: url(pink.png);
        background-repeat:  no-repeat;
        background-position:  bottom right;
        color:#000000;
    }
     QHeaderView::section {
    background-color: #F6DFEB;
    padding: 4px;
    border: 0px solid #F6DFEB;
}
    QToaster {
        border: 1px solid #F8EDED;
        border-radius: 4px; 
        background-color: #e4a2c2;
        color:#6dc263;
    }
    QLineEdit {
    background-color: #F8EDED;
    color:#000000;
    border: none;
    border-radius:8px;
    }
    QLineEdit::hover {
    border: 1px solid  #E4BAD4;
    }
    QScrollBar:vertical {
            border: 0px solid #E4BAD4;
            background-color: #E4BAD4;
            width:14px;    
            margin: 0px 0px 0px 3px;
        }
        QScrollBar::handle:vertical {         
            min-height: 0px;
            border: 0px solid red;
            border-radius: 5px;
            background-color: #E4BAD4;
        }
        QScrollBar::add-line:vertical {       
            height: 0px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }
        QScrollBar::sub-line:vertical {
            height: 0 px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }

'''