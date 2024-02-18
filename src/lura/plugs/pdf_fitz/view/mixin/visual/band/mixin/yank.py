from PyQt5 import QtCore
from gizmo.utils import tag

class Yank:

    @tag(['yy', 'yt'], modes=['visual[band]|^own'])
    def yankAsText(self, rstart=1, **kwargs):

        if not self.m_band: return
        i=self.m_band['item']
        e=i.element()
        b=self.m_band['box'][0]
        r=e.unity(b)
        r=(r.x(), r.y(), r.x()+r.width(), r.y()+r.height())
        f=e.getBlockText('blocks', clip=r)
        if not f: return
        t=f[0][4]
        if rstart==1: 
            t=t.replace('\n', ' ')
        if t:
            c=self.app.qapp.clipboard()
            c.setText(t)
        self.app.ui.moder.toggle()
        self.cleanUp()

    @tag('yi', modes=['visual[band]|^own'])
    def yankAsImage(self, *args, **kwargs):

        if not self.m_band: return
        i=self.m_band['item']
        b=self.m_band['box'][0]
        mb=i.mapToItem(b, unified=True)
        pxm=i.takePixmap()
        if not pxm: return
        crp=pxm.copy(mb.toRect())
        if crp:
            c=self.app.qapp.clipboard()
            c.setImage(crp.toImage())
        self.app.ui.moder.toggle()
        self.cleanUp()
