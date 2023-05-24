import os

from lura.utils import Plugin

class Display(Plugin):
    def __init__(self, app):
        super().__init__(app, name='generic')

    def toggleContinuousMode(self):
        self.app.window.view().toggleContinuousMode()

    def fitToPageWidth(self):
        self.app.window.view().fitToPageWidth()

    def fitToPageSize(self):
        self.app.window.view().fitToPageSize()

    def zoomIn(self):
        self.app.window.view().zoomIn()

    def zoomOut(self):
        self.app.window.view().zoomOut()

    def copy(self):
        pageItem=self.app.window.view().pageItem()
        text_list, area_list=pageItem.getCursorSelection()
        text=' '.join(text_list)
        if text: self.app.clipboard().setText(text)

    def paste(self):
        text=self.app.clipboard().text()
        os.popen(f'xdotool type {text}')
