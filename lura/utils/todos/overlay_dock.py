from PySide6.QtCore import Qt
from PySide6.QtWidgets import *


class OverlayWidget(QWidget):
    def __init__(self, window):
        QWidget.__init__(self, window)
        self.window = window

        self.collapse_threshold = 0.8
        self.down = 1

        self.label = QLabel("This is an overlay widget")
        self.label.setStyleSheet("background-color: rgba(100, 150, 100, 0.5)")

        self.size_grip = QLabel("...")
        self.size_grip.setStyleSheet("background-color: rgba(255, 0, 0, 0.5);")
        self.size_grip.setAlignment(Qt.AlignHCenter)
        self.size_grip.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        self.central_layout = QVBoxLayout()
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.addWidget(self.size_grip)
        self.central_layout.addWidget(self.label)

        self.setLayout(self.central_layout)


class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Overlay proof of concept")
        self.central_widget = QLabel(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n "
            "Sed euismod, urna eu tempor congue, nisi nisl aliquet "
            "nunc, euismod egestas nisl nisl euismod nunc.\n "
            "Sed euismod, urna eu tempor congue, nisi nisl aliquet "
            "nunc, euismod egestas nisl nisl euismod nunc. \n"
            "Sed euismod, urna eu tempor congue, nisi nisl aliquet "
            "nunc, euismod egestas nisl nisl euismod nunc. "
        )
        self.setCentralWidget(self.central_widget)

        self.error_widget = OverlayWidget(self)

        self.resize(800, 600)
        self.show()

        # Initially hide the widget
        self.error_widget.label.setVisible(False)
        self.error_widget.setGeometry(
            0,
            600 - self.error_widget.size_grip.height(),
            800,
            self.error_widget.size_grip.height(),
        )

    def mouseMoveEvent(self, event):
        if self.error_widget.size_grip.underMouse():
            self.update_error_widget(event.position().y())

    def update_error_widget(self, y):
        self.error_widget.down = y / self.height()
        self.error_widget.size_grip.setMaximumWidth(self.width())
        self.error_widget.size_grip.setMinimumWidth(self.width())

        if y < self.error_widget.size_grip.height():
            # Cursor over the window
            pass

        elif (1 - self.error_widget.down) < (1 - self.error_widget.collapse_threshold) / 2:
            # Hide the widget
            self.error_widget.label.setVisible(False)
            self.error_widget.setGeometry(
                0,
                self.height() - self.error_widget.size_grip.height(),
                self.width(),
                self.error_widget.size_grip.height(),
            )

        elif (1 - self.error_widget.down) > (1 - self.error_widget.collapse_threshold):
            # Default behavior
            self.error_widget.label.setVisible(True)
            self.error_widget.setGeometry(
                0,
                self.error_widget.down * self.height() - self.error_widget.size_grip.height(),
                self.width(),
                self.height() - self.error_widget.down * self.height(),
            )

        else:
            # Block the widget
            self.error_widget.label.setVisible(True)
            self.error_widget.setGeometry(
                0,
                self.error_widget.collapse_threshold * self.height() - self.error_widget.size_grip.height(),
                self.width(),
                self.height() - self.error_widget.collapse_threshold * self.height(),
            )

    def resizeEvent(self, event):
        # Hacky easy solution: hide the widget
        self.error_widget.label.setVisible(False)
        self.error_widget.setGeometry(
            0,
            self.height() - self.error_widget.size_grip.height(),
            self.width(),
            self.error_widget.size_grip.height(),
        )
        self.error_widget.size_grip.setMaximumWidth(self.width())
        self.error_widget.size_grip.setMinimumWidth(self.width())


app = QApplication()
window = Window()
app.exec()
