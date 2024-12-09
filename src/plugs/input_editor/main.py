from PyQt6 import QtGui, QtCore, QtWidgets

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
        mode=self.app.plugman.getPlug('Input')
        if mode:
            mode.addAgent('update', 'ElementView', self)
            mode.addAgent('populate', 'ElementView', self)

    def octivate(self, view=None, **kwargs):
        if view:
            view.setFocus()

    def activate(self, action=None, **kwargs):
        if action:
            func=getattr(self, action, None)
            if func:
                func(**kwargs)

    def populate(self, view=None, idx=None, nvim=None, **kwargs):
        if view:
            idx = idx or view.currentIndex()
            widget=view.widget(idx=idx)
            if widget and nvim:
                widget.setReadOnly(False)
                text=widget.toPlainText()
                nvim.setText(text)

    def update(self, view=None, nvim=None, widget=None, **kwargs):
        if not view:
            view=self.app.stateman.view()
        if view and not widget:
            data=view.widget('text')
            if data:
                widget, _ = data
        if widget and nvim:
            mode = nvim.mode()
            document=widget.document()
            widget.setPlainText(nvim.text())
            row, col = nvim.cursorPosition()
            byte_count=nvim.byte(row)
            # todo
            position=byte_count+col-1
            if col==0: position+=1
            print(row, col, position)
            print('bute: ', byte_count)
            cursor = QtGui.QTextCursor(document)
            cursor.setPosition(position)
            widget.setTextCursor(cursor)
            cond = mode != "i"
            cond = cond and mode != "v"
            cond = cond and mode != "V"
            cond = cond and mode != ""
            cond = cond and mode[0] != "c"
            selections = []
            cursor_mode=QtGui.QTextCursor.MoveMode
            cursor_op=QtGui.QTextCursor.MoveOperation
            if cond:
                sel = QtWidgets.QTextEdit.ExtraSelection()
                sel.cursor = cursor
                sel.cursor.movePosition(
                        cursor_op.NextCharacter, cursor_mode.KeepAnchor)
                sel.format = QtGui.QTextCharFormat()
                sel.format.setBackground(QtCore.Qt.GlobalColor.black)
                sel.format.setForeground(QtCore.Qt.GlobalColor.white)
                selections.append(sel)
            if mode in ["v", "V", ""]:
                row2, col2 = nvim.cursorAnchor()
                if row2 > 0 and col2 >= 0:
                    begin = nvim.byte(row, col)
                    end = nvim.byte(row2, col2)
                    if end <= begin + 1:
                        begin += 1
                        end -= 1
                    sel = QtWidgets.QTextEdit.ExtraSelection()
                    sel.cursor = QtGui.QTextCursor(document)
                    sel.cursor.setPosition(begin)
                    if mode == "V":
                        if begin <= end:
                            sel.cursor.movePosition(cursor_op.StartOfBlock)
                        else:
                            sel.cursor.movePosition(cursor_op.EndOfBlock)
                    sel.cursor.setPosition(end, cursor_mode.KeepAnchor)
                    if mode == "V":
                        if end <= begin:
                            sel.cursor.movePosition(
                                cursor_op.StartOfBlock, cursor_mode.KeepAnchor)
                        else:
                            sel.cursor.movePosition(
                                cursor_op.EndOfBlock, cursor_mode.KeepAnchor)
                    sel.format = QtGui.QTextCharFormat()
                    sel.format.setBackground(QtCore.Qt.GlobalColor.black)
                    sel.format.setForeground(QtCore.Qt.GlobalColor.white)
                    selections.append(sel)
            widget.setExtraSelections(selections)
