from PyQt6 import QtGui


def setEditorTabSize(editor, tab_stop):
    fm = QtGui.QFontMetrics(editor.font())
    stop_width = fm.width(" ") * tab_stop
    editor.setTabStopWidth(int(stop_width))
