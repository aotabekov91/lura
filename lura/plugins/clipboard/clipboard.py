import re

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lura.core import MapTree
from lura.view.docviewer import DocumentView

class Clipboard(QWidget):

    pathChosen = pyqtSignal(object)

    def __init__(self, parent, settings):
        super().__init__(parent)
        self.window = parent
        self.s_settings = settings
        self.clipboard = QApplication.clipboard()
        self.name = 'selector'

        self.globalKeys = {
            'Ctrl+r': (
                self.copyTextToClipboard,
                self.window,
                Qt.WindowShortcut)
        }


    def copyTextToClipboard(self):
        if type(self.window.view())!=DocumentView: return 
        self.window.plugin.view.cursor.activate(self, mode='rubberBand')
        self.window.plugin.view.cursor.rubberBandSelection.connect(
                self._copyTextToClipboard)


    def _copyTextToClipboard(self, rectF, pageItem):

        pageRect=self.getPageRect(rectF, pageItem)
        text=pageItem.page().text(pageRect)
        text=' '.join([f for f in text.split('\n') if f!=''])
        text=re.sub(re.compile(r'  *'), ' ', text)
        self.copyToClipboard(text)

    def copyToClipboard(self, text):
        self.clipboard.setText(text, QClipboard.Clipboard)

        if self.clipboard.supportsSelection():
            self.clipboard.setText(text, QClipboard.Selection)


    def getPageRect(self, rectF, pageItem):

        itemSize=pageItem.boundingRect()
        pageSize=pageItem.page().size()
        normTr=QTransform().scale(itemSize.width(), itemSize.height()).inverted()[0]
        normRectF=normTr.mapRect(rectF)
        pageTr=QTransform()
        pageTr.scale(pageSize.width(), pageSize.height())
        return pageTr.mapRect(normRectF)






