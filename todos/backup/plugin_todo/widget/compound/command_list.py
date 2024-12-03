from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .input_list import InputList

class CommandList (InputList):

    commandExecuted=pyqtSignal()
    commandExecuteFailed=pyqtSignal()
    deactivateCommandModeWanted=pyqtSignal()

    def __init__(self, **kwargs):

        super(CommandList, self).__init__(check_fields=['down'], 
                                          ignore_case=False, 
                                          exact_match=True,
                                          **kwargs,
                                          )

        self.timer=QTimer()
        self.timer.timeout.connect(self.executeByUnity)

        self.input.setLabel('Commands')

        self.returnPressed.connect(self.executeBySelection)

        self.inputTextChanged.connect(self.on_inputTextChanged)

    def on_inputTextChanged(self):

        self.timer.stop()
        if self.isVisible():
            if self.list.count()==1 and self.input.text(): self.timer.start(150)

    def executeByUnity(self):

        if self.list.count()==1: self.executeBySelection()

    def executeBySelection(self):

        self.deactivateCommandModeWanted.emit()
        item=self.list.currentItem()
        func=item.itemData.get('id', None)
        self.input.clear()
        if func: func()

            # try:
            #     func()
            #     self.commandExecuted.emit()
            # except:
            #     self.commandExecuteFailed.emit()

    def installEventFilter(self, listener):

        super().installEventFilter(listener)
        if hasattr(listener, 'deactivateCommandMode'):
            self.deactivateCommandModeWanted.connect(listener.deactivateCommandMode)

        dlist=[]

        for func_name in listener.__dir__():
            func=getattr(listener, func_name)
            if hasattr(func, 'key'):
                key=getattr(func, 'key', None)
                info=getattr(func, 'info', None)
                if not info: info=func_name
                data={'up': f'{info}', 'id':func}
                if key: data['down']=key
                dlist+=[data]

        if hasattr(listener, 'ui'):

            for func_name in listener.ui.__dir__():
                func=getattr(listener.ui, func_name)
                if hasattr(func, 'key'):
                    key=getattr(func, 'key', None)
                    info=getattr(func, 'info', None)
                    if not info: info=func_name
                    data={'up': f'{info}', 'id':func}
                    if key: data['down']=key
                    if not data in dlist: dlist+=[data]

        if not dlist: dlist=[{'up':'No commands found'}]

        self.setList(dlist)
