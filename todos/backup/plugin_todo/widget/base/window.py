from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Window (QMainWindow):

    def __init__ (self, central=None, title=None):

        super(Window, self).__init__()

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)

        if central: self.setCentralWidget(central)
        if title: self.setWindowTitle(title)
