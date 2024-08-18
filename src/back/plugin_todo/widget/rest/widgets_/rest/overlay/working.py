from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Overlay (QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setPalette(QPalette(Qt.transparent))
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.movie_screen = QLabel('test')
        
        # expand and center the label 
        self.movie_screen.setSizePolicy(QSizePolicy.Expanding, 
            QSizePolicy.Expanding)        
        self.movie_screen.setAlignment(Qt.AlignCenter) 
     

        main_layout = QVBoxLayout() 
        main_layout.addWidget(self.movie_screen)
        self.setLayout(main_layout) 
                
        # use an animated gif file you have in the working folder
        # or give the full file path
        self.movie = QMovie("giphy.gif", QByteArray(), self) 
        self.movie.setCacheMode(QMovie.CacheAll) 
        self.movie.setSpeed(100) 
        self.movie_screen.setMovie(self.movie) 
        self.movie.start()
        
    def paintEvent(self, e):

        qp = QPainter()
        qp.begin(self)
        qp.setBrush(QColor(255, 255, 255, 200))
        qp.drawRect(0, 0, 1000, 1000)
        qp.end()


class MainWindows(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        widget = QWidget()
        editor = QTextEdit('Lorem ipsum')
        layout = QGridLayout(widget)

        layout.addWidget(editor, 0,0,1,2)
        self.setCentralWidget(widget)

        self.overlay = Overlay(self.centralWidget())

    def resizeEvent(self, event):
        self.overlay.resize(event.size())
        QMainWindow.resizeEvent(self, event)


def main():
    app = QApplication([])
    win = MainWindows()
    win.setMinimumSize(500, 500)
    win.show()
    app.exec_()


if __name__ == '__main__':
    main()
