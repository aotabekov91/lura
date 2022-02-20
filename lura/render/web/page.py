from PyQt5.QtWebEngineWidgets import *

class WebPage(QWebEnginePage):

    def __init__(self, parent):
        super().__init__()
        self.m_document=parent

    def document(self):
        return self.m_document
