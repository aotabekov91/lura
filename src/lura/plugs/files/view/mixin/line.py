from PyQt5 import QtWidgets, QtGui, QtCore

class Line:

    def setup(self):

        super().setup()
        dline=LineDelegate(parent=self)
        self.setItemDelegate(dline)

class LineDelegate(QtWidgets.QStyledItemDelegate):

    def paint(self, p, o, i):

        tl=o.rect.topLeft()
        options=QtGui.QTextOption(QtCore.Qt.AlignCenter)
        x, y = tl.x(), tl.y() 
        v=self.parent()
        cr=v.currentIndex().row()
        r=str(abs(i.row()-cr))
        if (o.state & QtWidgets.QStyle.State_Selected):
            rect=QtCore.QRectF(0, y+1, 40, 20)
        else:
            rect=QtCore.QRectF(15, y+1, 40, 20)
        p.drawText(rect, r, options)
        tl.setX(x+55)
        o.rect.setTopLeft(tl)
        QtWidgets.QStyledItemDelegate.paint(self, p, o, i)

    def sizeHint(self, o, i):

        s=QtWidgets.QStyledItemDelegate.sizeHint(self, o, i)
        w=s.width()
        s.setWidth(w+55)
        return s
