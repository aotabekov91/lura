from PyQt5.QtCore import QRectF

def getPosition(boundaries):

    text=[]
    for b in boundaries: 
        x=str(b.x())[:6]
        y=str(b.y())[:6]
        w=str(b.width())[:6]
        h=str(b.height())[:6]
        text+=[f'{x}:{y}:{w}:{h}']
    return '_'.join(text)

def getBoundaries(position):

    areas=[]
    for t in position.split('_'):
        x, y, w, h = tuple(t.split(':'))
        areas+=[QRectF(
            float(x), 
            float(y), 
            float(w), 
            float(h)
            )]
    return areas
