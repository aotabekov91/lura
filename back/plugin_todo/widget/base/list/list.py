from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .items import IconUpDown

class ListWidget(QListWidget):

    hideWanted=pyqtSignal()
    openWanted=pyqtSignal()
    returnPressed=pyqtSignal()
    widgetDataChanged=pyqtSignal(object)

    def __init__(self, item_widget=IconUpDown, 

                 check_fields=['up', 'down'],
                 ignore_case=True,
                 exact_match=False,
                 enable_filter=True,
                 field_rematch=lambda x: x,
                 text_non_found='No match found',
                 **kwargs):

        super(ListWidget, self).__init__(**kwargs)

        self.dlist = []
        self.flist = []

        self.listener=None
        self.item_widget=item_widget
        self.exact_match=exact_match
        self.ignore_case=ignore_case
        self.check_fields=check_fields
        self.field_rematch=field_rematch
        self.enable_filter=enable_filter
        self.text_non_found=text_non_found

        self.setUI()

    def setUI(self):

        self.style_sheet = '''
            QListWidget{
                border-width: 0px;
                color: transparent;
                border-color: transparent; 
                background-color: transparent; 
                }
            QListWidget::item{
                border-style: outset;
                border-radius: 10px;
                border-style: outset;
                padding: 0px 0px 0px 0px;
                color: transparent;
                background-color: #101010;
                }
            QListWidget::item:selected {
                border-width: 3px;
                border-color: red;
                }
                '''

        self.setSpacing(2)

        self.setStyleSheet(self.style_sheet)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def installEventFilter(self, listener):

        super().installEventFilter(listener)
        self.listener=listener
        for i in range(self.count()):
            item=self.item(i)
            item.widget.installEventFilter(self.listener)

    def addItem(self, data):

        widget = self.item_widget(self, data)
        if self.listener: widget.installEventFilter(self.listener)

        super().addItem(widget.listItem())
        super().setItemWidget(widget.listItem(), widget)

    def widget(self): return self.item_widget(self)

    def move(self, crement=-1):

        self.setFocus()
        crow = self.currentRow()
        if crow==None: return
        crow += crement
        if crow < 0:
            crow = self.count()-1
        elif crow >= self.count():
            crow = 0

        self.setCurrentRow(crow)
        self.scrollToItem(
                self.currentItem(), 
                hint=QAbstractItemView.PositionAtTop)

        self.itemChanged.emit(self.currentItem())

    def sizeHint(self):

        hint=super().sizeHint()
        height=5
        if self.count()>0:
            for i in range(self.count()):
                height += self.item(i).sizeHint().height()
        hint.setHeight(height)
        return hint

    def setItem(self, condDict):

        for i in range(self.count()):
            item=self.item(i)
            data=item.itemData
            found=item
            for k, v in condDict.items():
                if data.get(k, None)!=v: return
            self.setCurrentItem(found)

    def setList(self, dlist, limit=30):

        if dlist is None: dlist=[]

        self.dlist=dlist
        self.flist=dlist

        self.addItems(dlist, limit=limit)

    def refresh(self, clear=False):

        tempList=self.filterList()
        if clear: tempList=self.dataList()
        crow=self.currentRow()

        self.addItems(tempList)
        self.setCurrentRow(crow)

    def setEnableFilter(self, condition): self.enable_filter=condition

    def unfilter(self): 

        if self.flist!=self.dlist: self.setList(self.dlist)

    def filter(self, text):

        if self.enable_filter:
            super().clear()
            if len(self.dlist)==0: 
                dlist=[{'up': text}] 
            else:
                if not text:
                    dlist=self.dlist
                else:
                    dlist=[]
                    tmp=self.widget()
                    for data in self.dlist:
                        if self.isin(text, data): dlist+=[data]

            self.setFilterList(dlist)
            self.setCurrentRow(0)

    def setFilterList(self, dlist):

        self.flist=dlist
        self.addItems(dlist)

    def isin(self, text, data):

        for f in self.check_fields:
            field_text= str(data.get(f, ''))
            if self.exact_match:
                if field_text and text==field_text[:len(text)]: return True
            else:
                if self.ignore_case:
                    if field_text and text.lower() in field_text.lower(): return True
                else:
                    if field_text and text in field_text: return True
        return False

    def dataList(self): return self.dlist

    def filterList(self): return self.flist

    def addItems(self, dlist, limit=30): 

        self.clear()

        if dlist:
            for i, data in enumerate(dlist):
                if limit and i>limit: break
                self.addItem(data)
            self.setCurrentRow(0)

        self.setCurrentRow(0)
        self.adjustSize()

    def keyPressEvent(self, event):

        if event.key() in [Qt.Key_J, Qt.Key_N]:
            self.move(crement=1)
        elif event.key() in [Qt.Key_K, Qt.Key_P]:
            self.move(crement=-1)
        elif event.key() in  [Qt.Key_M, Qt.Key_Enter]:
            self.returnPressed.emit()
        elif event.key() in [Qt.Key_Escape, Qt.Key_BracketLeft]:
            self.hideWanted.emit()
        elif event.key() == Qt.Key_L:
            self.openWanted.emit()
        elif event.modifiers() or self.hasFocus():
            if event.key() in [Qt.Key_N]:
                self.move(crement=1)
            elif event.key() in [Qt.Key_BracketLeft]:
                self.hideWanted.emit()
            elif event.key() in [Qt.Key_P]:
                self.move(crement=-1)
            elif event.key() in  [Qt.Key_M, Qt.Key_Return, Qt.Key_Enter]:
                self.returnPressed.emit()
            else:
                super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

    def adjustSize(self, width=None, height=None):

        if not width or not height: 

            if self.parent(): 
                width=self.parent().size().width()
                height=self.parent().size().height()
            else:
                width=self.size().width()
                height=self.size().height()

        self.setFixedWidth(width)
        self.setFixedHeight(height)

        for i in range(self.count()): self.item(i).widget.setFixedWidth(width)
        super().adjustSize()
