from PyQt6 import QtWebEngineWidgets, QtWidgets, QtCore

from plug_qt import vimo

class BrowserView(
        vimo.View,
        QtWidgets.QFrame,
):

    def setup(self):
        super().setup()
        self.m_browser=None
        self.setupBrowser()

    def browser(self):
        return self.m_browser

    def setupBrowser(self):

        self.m_browser=QtWebEngineWidgets.QWebEngineView()
        self.m_browser.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground)
        self.m_layout=QtWidgets.QHBoxLayout(self)
        self.m_layout.setContentsMargins(0, 0, 0, 0)
        self.m_layout.setSpacing(0)
        self.setLayout(self.m_layout)
        self.m_layout.addWidget(self.m_browser)

        # self.setStyleSheet('background-color: blue; padding: 20 20 20 20; border: 10px solid red;')

