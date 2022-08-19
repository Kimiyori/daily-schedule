
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc




class SpecialBG(qtw.QFrame):
    def __init__(self, *args, **kwargs):
        super(SpecialBG,self).__init__(*args, **kwargs)
        # mess with border-radius, thatDarklordGuy!
        qtw.QHBoxLayout(self)
        self.setObjectName('main')
        self.setStyleSheet("""QFrame#main{
                background-color: #F6DFEB;
                border-radius: 20px;
                }
                
                """)


class QToaster(qtw.QWidget):
    '''Widget showing specific notification depending on transmitted text'''

    def __init__(self, *args, **kwargs):
        super(QToaster, self).__init__(*args, **kwargs)
        self.VBox = qtw.QHBoxLayout()
        self.roundyround = SpecialBG(self)
        self.setWindowFlags(
            qtc.Qt.FramelessWindowHint  # hides the window controls
            | qtc.Qt.WindowStaysOnTopHint  # forces window to top... maybe
            | qtc.Qt.SplashScreen  # this one hides it from the task bar!
        )
        # alternative way of making base window transparent
        self.setAttribute(qtc.Qt.WA_TranslucentBackground, True)  # 100% transparent
        self.VBox.addWidget(self.roundyround)
        self.setLayout(self.VBox)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(15)
        self.setSizePolicy(qtw.QSizePolicy.Maximum,
                           qtw.QSizePolicy.Maximum)
        self.setFixedSize(250, 100)
        # alternatively:
        # self.setAutoFillBackground(True)
        # self.setFrameShape(self.Box)

        # here we set a timer,that triggered when timeout self.hide func and fade out at the end
        # self.timer = qtc.QTimer(singleShot=True, timeout=self.hide)

        # here we set the opacity effect for animation
        # self.opacityEffect = qtw.QGraphicsOpacityEffect(opacity=0)
        # and bind with self
        # self.setGraphicsEffect(self.opacityEffect)
        # create opacity animation
        self.opacityAni = qtc.QPropertyAnimation(self, b'windowOpacity')
        self.opacityAni.setStartValue(0.)
        self.opacityAni.setEndValue(1.)
        self.opacityAni.setDuration(100)

        self.corner = qtc.Qt.BottomRightCorner
        self.marginx = -100
        self.marginy = 100
        self.marginynew = 320

        # set corner and margin

    def checkClosed(self):
        # if we have been fading out, we're closing the notification
        self.close()

    def closeEvent(self, event):
        # as i understand deleteLater func need only for performans issues
        # we don't need the notification anymore, delete it!
        self.deleteLater()

    @staticmethod
    def showMessage(parent,message,
                    icon=qtw.QStyle.SP_MessageBoxInformation,
                    timeout=1500):
        self = QToaster(None)
        # This is a dirty hack!
        # parentless objects are garbage collected, so the widget will be
        # deleted as soon as the function that calls it returns, but if an
        # object is referenced to *any* other object it will not, at least
        # for PyQt (I didn't test it to a deeper level)
        self.__self = self

        currentScreen = qtw.QApplication.primaryScreen()
        reference = qtc.QRect(
            qtg.QCursor.pos() - qtc.QPoint(1, 1),
            qtc.QSize(3, 3))
        maxArea = 0

        parentRect = currentScreen.availableGeometry()
        # in sets in out timer time and after it finished out frame star fading
        # self.timer.setInterval(timeout)

        # use Qt standard icon pixmaps; see:
        # https://doc.qt.io/qt-5/qstyle.html#StandardPixmap-enum
        if isinstance(icon, qtw.QStyle.StandardPixmap):
            labelIcon = qtw.QLabel()
            self.roundyround.layout().addWidget(labelIcon, alignment=qtc.Qt.AlignLeft)
            icon = self.style().standardIcon(icon)
            size = self.style().pixelMetric(qtw.QStyle.PM_IconViewIconSize)
            labelIcon.setPixmap(icon.pixmap(size))
        # set message about succeess or fail
        self.label = qtw.QLabel(message)

        self.label.setObjectName('notification_text')
        self.roundyround.layout().addWidget(self.label, alignment=qtc.Qt.AlignLeft)

        self.closeButton = qtw.QToolButton()
        self.roundyround.layout().addWidget(self.closeButton)
        closeIcon = self.style().standardIcon(
            qtw.QStyle.SP_TitleBarCloseButton)
        self.closeButton.setIcon(closeIcon)
        self.closeButton.setAutoRaise(True)
        self.closeButton.clicked.connect(self.close)
        # here we start our timer
        # self.timer.start()
        #self.main_layout.addStretch()
        # raise the widget and adjust its size to the minimum
        self.raise_()
        self.adjustSize()

        geo = self.geometry()
        # now the widget should have the correct size hints, let's move it to the
        # right place
        geo.moveBottomRight(
            parentRect.bottomRight() + qtc.QPoint(self.marginx, -self.marginy))
        self.setGeometry(geo)
        self.show()


        self.opacityAni.start()
