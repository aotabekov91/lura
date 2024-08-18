from PyQt6 import QtCore

from plug import tag, Plug

class Cursor(Plug):

    def setup(self) -> None:
        super().setup()
        self.m_cursor=self.app.view.cursor()

    @tag("<c-a>c(normal)")
    def toggleCursor(self):
        blank = QtCore.Qt.CursorShape.BlankCursor
        arrow = QtCore.Qt.CursorShape.ArrowCursor
        if self.m_cursor == blank:
            self.m_cursor = arrow 
        else:
            self.m_cursor = blank
        self.app.view.setCursor(self.m_cursor)
