from PyQt6 import QtCore, QtGui, QtWidgets

from ...utils import setEditorTabSize
from .nvim import NVim


class VimEditor(QtWidgets.QTextEdit):
    modeChanged = QtCore.pyqtSignal(object)

    def __init__(
        self,
        vim=None,
        tab_stop=4,
        font="MS Gothic",
        objectName="Editor",
        **kwargs,
    ):
        self.mode = None
        self.abort = False
        self.tab_stop = tab_stop
        super().__init__(
            objectName=objectName,
            **kwargs,
        )

        self.setVim(vim)
        self.setFont(QtGui.QFont(font))
        setEditorTabSize(self, self.tab_stop)

    def setVim(self, nvim=None):
        if not nvim:
            nvim = NVim()
        self.nvim = nvim

    def setText(self, text):
        super().setText(text)
        self.nvim.setText(text)

    def keyPressEvent(self, e):
        key = e.text()
        if key:
            self.nvim.keyPress(key)
            while self.nvim.isBlocked():
                QtWidgets.QApplication.processEvents()
                if self.abort:
                    return
            self.update()
            self.updateMode()

    def text(self):
        return self.nvim.text()

    def clear(self):
        super().clear()
        self.nvim.setText("")
        # TODO: instead of jk [which is custom-specific] send Escape to return to normal mode from insert mode
        self.nvim.keyPress("jk")

    def updateMode(self):
        mode = self.nvim.mode()
        if self.mode != mode:
            self.mode = mode
            self.modeChanged.emit(mode)

    def update(self):
        mode = self.nvim.mode()
        self.setPlainText(self.text())
        row, col = self.nvim.cursorPosition()
        document=self.document()
        cursor = Qt.CursorShape.ui.QTextCursor(document)
        cursor.setPosition(self.nvim.byte(row, col))
        self.setTextCursor(cursor)
        selections = []
        cond = mode != "i"
        cond = cond and mode != "v"
        cond = cond and mode != "V"
        cond = cond and mode != ""
        cond = cond and mode[0] != "c"

        if mode == "i":
            self.setCursorWidth(1)
        elif mode == "n":
            self.setCursorWidth(0)

        if cond:
            selection = QtWidgets.QTextEdit.ExtraSelection()
            selection.cursor = cursor
            selection.cursor.movePosition(
                Qt.CursorShape.ui.QTextCursor.NextCharacter,
                Qt.CursorShape.ui.QTextCursor.KeepAnchor,
            )
            selection.format = QtGui.QTextCharFormat()
            selection.format.setBackground(QtCore.Qt.black)
            selection.format.setForeground(QtCore.Qt.white)
            selections.append(selection)

        if mode == "v" or mode == "V" or mode == "":
            row2, col2 = self.nvim.cursorAnchor()
            if row2 > 0 and col2 >= 0:
                begin = self.nvim.byte(row, col)
                end = self.nvim.byte(row2, col2)

                if end <= begin + 1:
                    begin += 1
                    end -= 1

                selection = (
                    QtWidgets.QTextEdit.ExtraSelection()
                )
                selection.cursor = (
                    Qt.CursorShape.ui.QTextCursor(
                        self.document()
                    )
                )
                selection.cursor.setPosition(begin)
                if mode == "V":
                    if begin <= end:
                        selection.cursor.movePosition(
                            Qt.CursorShape.ui.QTextCursor.StartOfBlock
                        )
                    else:
                        selection.cursor.movePosition(
                            Qt.CursorShape.ui.QTextCursor.EndOfBlock
                        )

                selection.cursor.setPosition(
                    end,
                    Qt.CursorShape.ui.QTextCursor.KeepAnchor,
                )
                if mode == "V":
                    if end <= begin:
                        selection.cursor.movePosition(
                            Qt.CursorShape.ui.QTextCursor.StartOfBlock,
                            Qt.CursorShape.ui.QTextCursor.KeepAnchor,
                        )
                    else:
                        selection.cursor.movePosition(
                            Qt.CursorShape.ui.QTextCursor.EndOfBlock,
                            Qt.CursorShape.ui.QTextCursor.KeepAnchor,
                        )

                selection.format = QtGui.QTextCharFormat()
                selection.format.setBackground(
                    QtCore.Qt.black
                )
                selection.format.setForeground(
                    QtCore.Qt.white
                )
                selections.append(selection)
        self.setExtraSelections(selections)
