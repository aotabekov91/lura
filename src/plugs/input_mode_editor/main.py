from PyQt6 import QtGui, QtCore

from plug import Plug

class EditorInputMode(Plug):

    def setup(self):
        super().setup()
        if self.app.running:
            self.addAgent()
        else:
            self.app.appSoonStarts.connect(
                    self.addAgent)

    def addAgent(self):
        input_mode=self.app.plugman.getPlug('InputMode')
        if input_mode:
            input_mode.addAgent('EditorView', self)

    def octivate(self, view=None, **kwargs):
        if view:
            view.setFocus()

    def activate(self, view=None, kind=None, **kwargs):
        if view and kind:
            functor=getattr(self, kind, None)
            if functor:
                functor(view=view, **kwargs)

    def insert(self, view=None, xrange=[1], widget=None, **kwargs):
        if not widget:
            data=view.widget('text')
            if data:
                widget, _ = data
        if widget:
            widget.setReadOnly(False)
            widget.setFocus()

    def append(self, view=None, xrange=[1], widget=None, **kwargs):
        if not widget:
            data=view.widget('text')
            if data:
                widget, _ = data
        if widget:
            widget.setReadOnly(False)
            position = QtGui.QTextCursor.MoveOperation.End
            cursor = widget.textCursor()
            cursor.movePosition(position)
            widget.setTextCursor(cursor)
            widget.setFocus()
