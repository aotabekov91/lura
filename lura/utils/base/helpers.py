#!/usr/bin/python3

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

def register(func):
    def inner(plugin, *args, **kwargs):
        key=f'{plugin.__class__.__name__}_{func.__name__}'
        plugin.app.actions[key]=func
        return func(plugin, *args, **kwargs)
    return inner

def getPosition(boundaries):
    start=boundaries[0]
    end=boundaries[-1]
    topLeft=start.topLeft()
    x, y=topLeft.x(), topLeft.y()
    bottomRight=start.bottomRight()
    x_, y_=bottomRight.x(), bottomRight.y()
    first_line=':'.join(str(round(f, 5)) for f in [x, y, x_, y_])
    topLeft=end.topLeft()
    x, y=topLeft.x(), topLeft.y()
    bottomRight=end.bottomRight()
    x_, y_=bottomRight.x(), bottomRight.y()
    last_line=':'.join(str(round(f, 5)) for f in [x, y, x_, y_])
    return f'{first_line}_{last_line}'

def getBoundaries(position):
    first_line, last_line =tuple(position.split('_'))
    x, y, x_, y_ =tuple([float(f) for f in first_line.split(':')])
    firstRect=QRectF()
    firstRect.setTopLeft(QPointF(x, y))
    firstRect.setBottomRight(QPointF(x_, y_))
    x, y, x_, y_ =tuple([float(f) for f in last_line.split(':')])
    lastRect=QRectF()
    lastRect.setTopLeft(QPointF(x, y))
    lastRect.setBottomRight(QPointF(x_, y_))
    if first_line==last_line:
        recs=[firstRect]
    else:
        recs=[firstRect, lastRect]
    return recs
