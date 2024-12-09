from PyQt6 import QtGui

from plug import Plug

class ElementListEdit(Plug):

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
            input_mode.addAgent('insert', 'ElementListView', self)
            input_mode.addAgent('append', 'ElementListView', self)

    def activate(self, view=None, kind=None, **kwargs):
        if view and kind:
            functor=getattr(self, kind, None)
            if functor:
                functor(view=view, **kwargs)

    def octivate(self, view=None, **kwargs):
        if view:
            view.setFocus()

    def insert(self, view=None, xrange=[1], widget=None, **kwargs):
        if not widget and view:
            item=view.currentItem()
            if item:
                view_widget=view.itemWidget(item)
                data=view_widget.widget('text')
                if data:
                    widget, _ = data
        if widget:
            widget.setReadOnly(False)
            widget.setFocus()

    def append(self, view=None, xrange=[1], widget=None, **kwargs):
        if not widget and view:
            item=view.currentItem()
            if item:
                view_widget=view.itemWidget(item)
                data=view_widget.widget('text')
                if data:
                    widget, _ = data
        if widget:
            widget.setReadOnly(False)
            position = QtGui.QTextCursor.MoveOperation.End
            cursor = widget.textCursor()
            cursor.movePosition(position)
            widget.setTextCursor(cursor)
            widget.setFocus()
