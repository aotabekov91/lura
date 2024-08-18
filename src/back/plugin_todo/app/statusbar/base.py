from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..utils import register
from ..plugin import Configure

class StatusBar(QStatusBar):

    hideWanted=pyqtSignal()
    keyPressEventOccurred=pyqtSignal(object)

    def __init__(self, window):

        super(StatusBar, self).__init__()

        self.clients={}

        self.window=window
        self.configure=Configure(
                window.app, 
                'Statusbar', 
                self, 
                mode_keys={'command': 's'})

        self.setUI()
        self.hide()

        self.window.display.viewChanged.connect(self.on_viewChanged)
        self.window.display.itemChanged.connect(self.on_itemChanged)

    def setUI(self):

        self.style_sheet='''
            QLineEdit {
                background-color: transparent;
                border-color: transparent;
                border-width: 0px;
                border-radius: 0px;
                }
            QLabel{
                background-color: transparent;
                }
                '''

        layout=self.layout()
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)

        self.info=QLabel('Info')
        self.page=QLabel('Page')
        self.edit=QLineEdit(self)
        self.detail=QLabel('Detail')
        self.model=QLabel('Document')

        self.setFixedHeight(25)

        self.addWidget(self.info)
        self.addWidget(self.edit, 1)
        self.addWidget(self.detail)

        self.addPermanentWidget(self.model)
        self.addPermanentWidget(self.page, 0)

        self.info.hide()
        self.edit.hide()
        self.detail.hide()

        self.setSizeGripEnabled(False)
        self.setStyleSheet(self.style_sheet)

    def installEventFilter(self, listener):

        super().installEventFilter(listener)
        self.info.installEventFilter(listener)
        self.page.installEventFilter(listener)
        self.detail.installEventFilter(listener)
        self.model.installEventFilter(listener)

    def removeEventFilter(self, listener):

        super().removeEventFilter(listener)
        self.info.removeEventFilter(listener)
        self.edit.removeEventFilter(listener)
        self.page.removeEventFilter(listener)
        self.detail.removeEventFilter(listener)
        self.model.removeEventFilter(listener)

    def on_viewChanged(self, view): 

        if view.name(): self.model.setText(str(view.name()))

    def on_itemChanged(self, view, item): 

        if item.name(): self.page.setText(str(item.name()))

    @register('i', modes=['normal', 'command'])
    def toggle(self):

        if self.isVisible():
            self.hide()
        else:
            self.show()

    def clear(self, fields=['info', 'edit', 'detail']):

        for f in fields:
            field=getattr(self, f)
            field.setText('')
            field.hide()

    def setData(self, data=None):

        self.clear()

        if not data: data=self.clients.get('prev', {})

        self.clients['prev']=self.clients.get('current', {})
        if 'client' in self.clients['prev']:
            self.clients['prev']['visible']=self.isVisible()
        self.clients['current']=data

        for f, v in data.items():
            if f in ['edit', 'info', 'detail', 'page', 'model']:
                field=getattr(self, f, None)
                if field:
                    field.setText(v)
                    field.show()

        if data.get('visible', False): 
            self.show()
        else:
            super().hide()

    def hide(self):

        data=self.clients.get('prev', {})
        self.setData(data)

        if not getattr(data, 'visible', False): super().hide()

    def keyPressEvent(self, event):

        self.keyPressEventOccurred.emit(event)
        if event.key()==Qt.Key_Escape:
            self.hide()
            self.hideWanted.emit()
        elif event.key()==Qt.Key_I and self.edit.isVisible():
            self.edit.setFocus()
        else:
            super().keyPressEvent(event)
