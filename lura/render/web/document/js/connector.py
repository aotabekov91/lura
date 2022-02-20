from PyQt5.QtCore import *

class JSConnector(QObject):

    loadAnnotations=pyqtSignal('QJsonArray')
    jsAnnotationCreated=pyqtSignal('QJsonObject')

    def __init__(self, parent):
        super().__init__(parent)
        self.m_document=parent

    @pyqtSlot('QJsonObject')
    def annotationCreated(self, data):
        self.jsAnnotationCreated.emit(data)

    @pyqtSlot(int)
    def width(self, m_width):
        self.m_document.on_fitToPageWidth(m_width)
