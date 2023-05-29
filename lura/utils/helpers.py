from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

def register(key=None, info=None, modes=[]):

    def _key(func):
        def inner(self, *args, **kwargs): 
            return func(self, *args, **kwargs)
        inner.key=key
        inner.info=info
        inner.modes=modes
        inner.func=func
        inner.name=func.__name__
        return inner
    return _key

def watch(widget='window', context=Qt.WidgetWithChildrenShortcut, info=None):
    def _watch(func):
        def inner(self, *args, **kwargs):
            return func(self, *args, **kwargs)
        inner.info=info
        inner.widget=widget
        inner.context=context
        return inner
    return _watch

def getPosition(boundaries):

    text=[]
    for b in boundaries:
        text+=[f'{b.x()}:{b.y()}:{b.width()}:{b.height()}']
    return '_'.join(text)

    # start=boundaries[0]
    # end=boundaries[-1]
    # topLeft=start.topLeft()
    # x, y=topLeft.x(), topLeft.y()
    # bottomRight=start.bottomRight()
    # x_, y_=bottomRight.x(), bottomRight.y()
    # first_line=':'.join(str(round(f, 5)) for f in [x, y, x_, y_])
    # topLeft=end.topLeft()
    # x, y=topLeft.x(), topLeft.y()
    # bottomRight=end.bottomRight()
    # x_, y_=bottomRight.x(), bottomRight.y()
    # last_line=':'.join(str(round(f, 5)) for f in [x, y, x_, y_])
    # return f'{first_line}_{last_line}'

def getBoundaries(position):

    areas=[]
    for t in position.split('_'):
        x, y, w, h = tuple(t.split(':'))
        areas+=[QRectF(float(x), float(y), float(w), float(h))]
    return areas

    # first_line, last_line =tuple(position.split('_'))
    # x, y, x_, y_ =tuple([float(f) for f in first_line.split(':')])
    # firstRect=QRectF()
    # firstRect.setTopLeft(QPointF(x, y))
    # firstRect.setBottomRight(QPointF(x_, y_))
    # x, y, x_, y_ =tuple([float(f) for f in last_line.split(':')])
    # lastRect=QRectF()
    # lastRect.setTopLeft(QPointF(x, y))
    # lastRect.setBottomRight(QPointF(x_, y_))
    # if first_line==last_line:
    #     recs=[firstRect]
    # else:
    #     recs=[firstRect, lastRect]
    # return recs
