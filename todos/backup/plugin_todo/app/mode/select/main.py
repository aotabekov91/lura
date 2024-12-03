from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from plugin.app import register
from plugin.app.mode import Visual as Mode

class Select(Mode): pass

    def __init__(self, app):

        super().__init__(app)

        self.hints=None
        self.hinting=False
        self.selection=None

    @register('j')
    def down(self): self.move(kind='down')

    @register('k')
    def up(self): self.move(kind='up')

    @register('h')
    def left(self): self.move(kind='left')

    @register('l')
    def right(self): self.move(kind='right') 

    def move(self, kind):

        view=self.app.main.display.view
        if view and view.selected(): 

            container=view.selected()[0]
            layout=container.widget.attribute_layout
            if not container.widget.current:
                row=0
                col=0
            else:
                row=container.widget.current.item_row
                col=container.widget.current.item_column
                if kind=='down':
                    row+=1
                    if row>= layout.rowCount(): row=0
                elif kind=='up':
                    row-=1
                    if row<0: row = layout.rowCount()-1
                elif kind=='right':
                    col+=1
                    if col>=layout.columnCount(): col=0
                elif kind=='left':
                    col-=1
                    if col<0: col=layout.columnCount()-1

            widget=layout.itemAt(row, col)
            if widget: widget.setSelected(True)
