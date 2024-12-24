from PyQt6 import QtWebEngineWidgets, QtWidgets, QtCore

from plug_qt import vimo

class BrowserView(
        vimo.View,
        QtWidgets.QWidget,
):

    def setup(self):
        super().setup()
        self.m_browser=None
        self.setupBrowser()

    def browser(self):
        return self.m_browser

    def setupBrowser(self):
        self.m_layout=QtWidgets.QHBoxLayout(self)
        self.m_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.m_layout)
        self.m_browser=QtWebEngineWidgets.QWebEngineView()
        self.m_layout.setSpacing(0)
        self.m_layout.addWidget(self.m_browser)
        self.m_layout.addWidget(QtWidgets.QLabel('test'))
        self.m_browser.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground)
