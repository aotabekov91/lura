from PyQt6 import QtWebEngineWidgets

from plug_qt import vimo

class HelpView(
    vimo.View,
    QtWebEngineWidgets.QWebEngineView,
):
    isSubview=True
    canFollow = True
    position = {"HelpView": "C|x"}

    def setup(self):
        super().setup()
        self.m_model=None
        self.m_current=None

    def setModel(self, model):
        if id(self.m_model) != id(model):
            html=model.modelData()
            self.setHtml(html)

    def count(self):
        return 100

    def currentIndex(self):
        return self.m_current

    def setCurrentIndex(self, idx):
        if self.m_current != idx:
            current, previous = idx, self.m_current
            self.m_current, self.m_previous = current, previous
        self.indexChanged.emit(self.m_current)
