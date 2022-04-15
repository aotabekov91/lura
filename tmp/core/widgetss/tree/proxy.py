from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class BaseProxyWidget(QGraphicsWidget):

    sizeChanged=pyqtSignal()
    pushButtonClicked=pyqtSignal(object)

    def __init__(self, widget, item):
        super().__init__()
        self.m_widget=widget
        self.m_item=item
        self.setup()

    def widget(self):
        return self.m_widget

    def setFixedWidth(self, width):
        self.m_widget.setFixedWidth(width)

    def setStyleSheetButton(self, style):
        self.m_button.widget().setStyleSheet(style)

    def setStyleSheetWidget(self, style):
        self.m_widget.setStyleSheet(style)

    def bottomLeft(self):
        return self.pos().x(), self.pos().y()+self.height()

    def height(self):
        return self.m_widget.height()

    def width(self):
        return self.m_widget.width()

    def setup(self):

        self.assignProxy()
        self.assignButton()

    def change(self, kind):
        self.setFocus()
        self.m_widget.change(kind)

    def toggle(self, kind):
        self.m_widget.toggle(kind)

    def assignProxy(self):
        layout=QGraphicsLinearLayout(self)

        proxyE=QGraphicsProxyWidget()
        proxyE.setWidget(self.m_widget)
        layout.addItem(proxyE)
        layout.setContentsMargins(0, 0, 0, 0)

    def assignButton(self, item=None):
        pushButton = QPushButton('>')
        pushButton.resize(QSize(20, 20))
        pushButton.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        pushButton.clicked.connect(lambda: self.pushButtonClicked.emit(self.m_item))
        button = QGraphicsProxyWidget()
        button.setWidget(pushButton)
        self.m_button=button

    def setPos(self, x, y):
        self.m_button.setPos(0, y)
        super().setPos(x, y)

    def button(self):
        return self.m_button

    def hide(self):
        self.m_button.hide()
        super().hide()

        for index in range(self.m_item.rowCount()):
            self.m_item.child(index).proxy().hide()

    def show(self):
        self.m_button.show()
        super().show()
