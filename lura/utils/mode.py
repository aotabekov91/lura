import inspect

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from plugin import ListWidget
from lura.utils import BaseCommandStack

from .plugin import Plugin

class Mode(Plugin):

    returnPressed=pyqtSignal()
    listenWanted=pyqtSignal(str)
    delistenWanted=pyqtSignal(str)

    def __init__(self, app, 

                 wait_time=250,
                 listening=False,
                 position='bottom',
                 listen_leader=None,
                 show_commands=False,
                 show_statusbar=False,
                 delisten_on_exec=True,
                 delisten_wanted='normal',
                 listen_widget=[],
                 exclude_widget=[],
                 **kwargs):

        self.commands=[]
        self.keys_pressed=[]
        self.wait_time=wait_time
        self.listening=listening

        self.show_commands=show_commands
        self.listen_widget=listen_widget
        self.listen_leader=listen_leader
        self.exclude_widget=exclude_widget

        self.show_statusbar=show_statusbar
        self.delisten_wanted=delisten_wanted
        self.delisten_on_exec=delisten_on_exec

        super(Mode, self).__init__(app, position=position, command_leader=[], **kwargs)

        self.timer=QTimer()
        self.timer.timeout.connect(self.delisten)

        self.setUI()
        self.setBarData()

        self.app.modes.addMode(self)
        self.app.installEventFilter(self)

    def setBarData(self):
        
        self.data={
                'detail': '',
                'client': self,
                'visible': self.show_statusbar,
                'info':f'[{self.name.title()}]',
                }

    def actOnDefocus(self): pass

    def actOnFocus(self): pass

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
                    if hasattr(plugin, 'modeKey'): 
                        prefix=plugin.modeKey(self.name)
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

        self.app.modes.delisten()

        self.app.main.bar.setData(self.data)
        self.listening=True

    def confirm(self):
        
        self.returnPressed.emit()

        if self.ui.mode.isVisible():

            item=self.ui.mode.item(self.ui.mode.currentRow())
            if item:
                matches=[item.itemData]
                self.reportMatches(matches, [])
                self.runMatches(matches, [], None, None)

    def checkListenWanted(self, widget, event): return True

    def eventFilter(self, widget, event):

        if self.listen_leader or self.listening:

            if event.type()==QEvent.KeyPress:
                
                if self.listening:

                    cond1=True 
                    if self.listen_widget:
                        if not widget in self.listen_widget: cond1=False

                    cond2=True
                    if self.exclude_widget:
                        if widget in self.exclude_widget: 
                            cond2=False

                    if cond1 and cond2:

                        mode=None

                        if self.name=='normal':
                            mode=self.app.modes.leaders.get(event.text(), None)

                        if mode: 
                            self.app.modes.setMode(mode.name)
                            event.accept()
                            return True 

                        if event.key() in  [Qt.Key_Enter, Qt.Key_Return]: 

                            self.confirm()
                            event.accept()
                            return True
                                
                        if event.key()==Qt.Key_Backspace:

                            self.clearKeys()
                            event.accept()
                            return True

                        if event.key()==Qt.Key_Escape or event.text() == self.listen_leader:

                            if self.name!='normal':

                                self.delistenWanted.emit(self.delisten_wanted)
                                event.accept()
                                return True

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

                        self.addKeys(event)
                        event.accept()
                        return True

        return super().eventFilter(widget, event)

    def clearKeys(self):

        self.timer.stop()
        self.keys_pressed=[]
        self.app.main.bar.detail.clear()
        self.ui.mode.unfilter()

    def delisten(self):

        self.clearKeys()
        self.listening=False

        if self.ui.activated: self.ui.deactivate()
        if self.show_statusbar: self.app.main.bar.setData()

    def listen(self):

        self.listening=True

        self.clearKeys()
        self.app.main.bar.setData(self.data)

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
        
        moddies=QApplication.keyboardModifiers()

        text=event.text()

        # if not text and moddies & Qt.ShiftModifier: 
        #     text='Shift'
        # if not text and moddies & Qt.ControlModifier: 
        #     text='Ctrl'
        
        if text: self.keys_pressed+=[text]

        return text

    def reportMatches(self, matches, partial):

        if self.ui.isVisible(): self.ui.mode.setFilterList(matches+partial)
        self.app.main.bar.detail.setText(
                f'{"".join(self.keys_pressed)}')

    def runMatches(self, matches, partial, key, digit):

        self.timer.timeout.disconnect()
        self.timer.timeout.connect(lambda: self.executeMatch(matches, partial, digit))
        if len(matches)==1 and not partial:
            self.timer.start(0)
        else:
            if self.wait_time: self.timer.start(self.wait_time)

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

        self.app.modes.setMode(self.delisten_wanted)
        # self.delistenWanted.emit(self.delisten_wanted)

    def toggleCommands(self):

        if self.ui.mode.isVisible():
            self.ui.deactivate()
        else:
            self.ui.activate()
            self.ui.show(self.ui.mode)
