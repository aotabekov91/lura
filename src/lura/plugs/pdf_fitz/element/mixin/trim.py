from PyQt5 import QtCore

class Trim:

    def findTrimRect(self, img):

        w=img.width
        h=img.height
        scol=img.pixel(0, 0)

        leftx=0
        found=False
        while w>leftx:
            for y in range(h):
                pxl=img.pixel(leftx, y)
                if scol!=pxl: 
                    found=True
                    break
            if found:break
            leftx+=1

        found=False
        rightx=w-1
        while rightx>-1:
            for y in range(h):
                pxl=img.pixel(rightx, y)
                if scol!=pxl: 
                    found=True
            if found:break
            rightx-=1
        rightx+=1

        topy=0
        found=False
        while h>topy:
            for x in range(w):
                pxl=img.pixel(x, topy)
                if scol!=pxl: 
                    found=True
                    break
            if found:break
            topy+=1

        bottomy=h-1
        found=False
        while bottomy>0:
            for x in range(w):
                pxl=img.pixel(x, bottomy)
                if scol!=pxl: 
                    found=True
                    break
            if found:break
            bottomy-=1
        bottomy+=1
        return QtCore.QRectF(
                leftx, topy, rightx, bottomy)

    # def setup(self):

    #     super().setup()
    #     self.m_trect=None
    #     self.setTrim()

    # def setTrim(self):
    #     if not self.m_trect:
    #         p=self.m_data.get_pixmap()
    #         trect=self.findTrimRect(p)
    #         self.m_trect=self.unify(trect)
    #         self.m_trim_trans=QtGui.QTransform()
    #         self.m_size=trect.size()
