import inspect

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from plugin import ListWidget
from lura.utils import BaseCommandStack

from .plugin import Plugin

class Mode(Plugin):

    returnPressed=pyqtSignal()
    delistenWanted=pyqtSignal()
    listenWanted=pyqtSignal(str)

    def __init__(self, app, 

                 wait_time=250,
                 show_commands=False,
                 show_statusbar=False,
                 delisten_on_exec=True,
                 **kwargs):

        self.client=None
        self.commands=[]
        self.keys_pressed=[]
        self.wait_time=wait_time
        self.show_commands=show_commands
        self.show_statusbar=show_statusbar
        self.delisten_on_exec=delisten_on_exec

        super(Mode, self).__init__(app, position='bottom', command_leader=[], **kwargs)

        self.timer=QTimer()
        self.timer.timeout.connect(self.delisten)

        self.setUI()
        self.setBarData()

        self.app.installEventFilter(self)

    def setBarData(self):
        
        self.data={
                'info': f'[{self.name.title()}]',
                'detail': '',
                'client': self,
                'visible': self.show_statusbar,
                }

        if getattr(self, 'client', None):
            self.data['info']=f'[{self.client.name.title()}]'

    def setClient(self, client=None): 

        self.commands=[]

        self.client=client
        if self.client:
            self.name=self.client.name
            self.setBarData()
            self.data.update(self.client.bar_data)
            self.name='plug'
            if self.client.listening:
                self.listen_widget=self.client.listen_widget
                self.exclude_widget=self.client.exclude_widget
                self.setPluginData(self.client, self.app.manager.actions[self.client])
                self.commands=sorted(self.commands, key=lambda x: x['plugin'])

    def setData(self):

        self.commands=[]

        for plugin, actions in self.app.manager.actions.items():
            self.setPluginData(plugin, actions, self.name)

        #own actions
        self.setPluginData(self, self.app.manager.actions[self])

        self.commands=sorted(self.commands, key=lambda x: x['plugin'])
        self.ui.mode.setList(self.commands)

    def setPluginData(self, plugin, actions, mode_name=None):

        for (plugin_name, func_name), method in actions.items():
            if not mode_name or  mode_name in method.modes:
            # if not mode_name or plugin_name==self.name or  mode_name in method.modes:
                method_name=getattr(method, 'info', None)
                if method_name: func_name=method_name
                name=f'[{plugin_name}] {func_name}'
                data={'id': method, 'up': name, 'plugin': plugin_name}
                if method.key: 
                    key=method.key
                    if hasattr(plugin, 'modeKeys'): 
                        prefix=plugin.modeKeys(self.name)
                        key=f'{prefix}{key}'
                    data['down']=key
                self.commands+=[data]

    def setUI(self):
        
        super().setUI()

        mode=ListWidget(exact_match=True, check_fields=['down'])

        self.ui.addWidget(mode, 'mode')
        self.ui.mode.hideWanted.connect(self.deactivate)
        self.ui.mode.returnPressed.connect(self.confirm)
        self.ui.focusGained.connect(self.activate)
        self.ui.installEventFilter(self)

    def activate(self):

        self.app.modes.listen(self.name)
        self.app.window.bar.setData(self.data)

    def confirm(self):
        
        self.returnPressed.emit()

        if self.ui.mode.isVisible():

            item=self.ui.mode.item(self.ui.mode.currentRow())
            if item:
                matches=[item.itemData]
                self.reportMatches(matches, [])
                self.runMatches(matches, [], None, None)

    def eventFilter(self, widget, event):

        if self.client and not self.client.listening: return False

        if self.listen_leader or self.listening:

            if event.type()==QEvent.KeyPress:

                print(self.__class__.__name__, event.text())

                cond1=not self.listen_widget or widget in self.listen_widget
                cond2=not widget in self.exclude_widget

                if cond1 and cond2:

                    if not self.listening and event.text() == self.listen_leader:

                        self.listenWanted.emit(self.name)
                        event.accept()
                        return True

                    elif self.listening:

                        if event.modifiers() and self.ui.isVisible():

                            if event.key() in [Qt.Key_N, Qt.Key_J]:
                                self.ui.mode.move(crement=1)
                                event.accept()
                                return True

                            elif event.key() in [Qt.Key_P, Qt.Key_K]:
                                self.ui.mode.move(crement=-1)
                                event.accept()
                                return True

                            elif event.key() in  [Qt.Key_M, Qt.Key_L]: 
                                self.confirm()
                                event.accept()
                                return True
                                
                            elif event.key() in  [Qt.Key_Enter, Qt.Key_Return]: 
                                self.confirm()
                                event.accept()
                                return True
                                
                        elif event.key() in  [Qt.Key_Enter, Qt.Key_Return]: 
                            self.confirm()
                            event.accept()
                            return True
                                
                        elif event.key()==Qt.Key_Backspace:
                            self.clearKeys()
                            event.accept()
                            return True

                        elif event.key()==Qt.Key_Escape or event.text() == self.listen_leader:
                            self.delistenWanted.emit()
                            event.accept()
                            return True

                        elif event.text() != self.listen_leader:
                            self.addKeys(event)
                            event.accept()
                            return True

        return super().eventFilter(widget, event)

    def clearKeys(self):

        self.timer.stop()
        if self.keys_pressed:

            self.keys_pressed=[]
            self.ui.mode.unfilter()
            self.app.window.bar.detail.clear()

    def delisten(self, force=True):

        self.clearKeys()
        self.setBarData()
        if force:
            self.listening=False
            self.ui.deactivate()
            self.app.window.bar.setData()

    def listen(self):

        self.listening=True
        self.keys_pressed=[]
        self.app.window.bar.setData(self.data)

        if self.show_commands: 
            self.ui.activate()
            self.ui.show(self.ui.mode)

    def addKeys(self, event):

        self.timer.stop()
        if self.registerKey(event):
            key, digit = self.getKeys()
            matches, partial=self.getMatches(key, digit)
            self.reportMatches(matches, partial)
            self.runMatches(matches, partial, key, digit)

    def registerKey(self, event):
        
        text=event.text()
        if text: self.keys_pressed+=[text]
        return text

    def reportMatches(self, matches, partial):

        if self.ui.isVisible(): self.ui.mode.setFilterList(matches+partial)
        self.app.window.bar.detail.setText(
                f'{"".join(self.keys_pressed)}')

    def runMatches(self, matches, partial, key, digit):

        self.timer.timeout.disconnect()
        self.timer.timeout.connect(lambda: self.executeMatch(matches, partial, digit))
        if len(matches)==1 and not partial:
            self.timer.start(0)
        else:
            self.timer.start(self.wait_time)

    def getKeys(self):

        key=''
        digit=''
        for i, k in enumerate(self.keys_pressed):
            if k.isnumeric():
                digit+=k
            else:
                key=''.join(self.keys_pressed[i:])
                break
        if digit: 
            digit=int(digit)
        else:
            digit=None

        return key, digit

    def getMatches(self, key, digit):

        exact=[]
        partial=[]
        for data in self.commands:
            func=self._getFunc(data)
            k=data['down']
            if key==k[:len(key)]: 
                if digit:
                    if not 'digit' in inspect.signature(func).parameters: continue
                if key==k:
                    exact+=[data]
                elif key==k[:len(key)]: 
                    partial+=[data]
        return exact, partial

    def executeMatch(self, matches, partial, digit):

        if not partial:

            if not matches:
                self.clearKeys()
                self.listen()
            elif len(matches)==1:
                self.clearKeys()
                if self.delisten_on_exec: self._onExecuteMatch()

                match=matches[0]['id']
                if digit and 'digit' in inspect.signature(match.func).parameters:
                    match(digit=digit)
                else:
                    match()

    def _getFunc(self, data):
        return data['id'].func

    def _onExecuteMatch(self):
        self.delistenWanted.emit()
