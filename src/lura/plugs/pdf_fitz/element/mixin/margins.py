from PyQt5 import QtGui, QtCore

class TrimMargins:

    def trimMargins(self, img, bg='white'):

        rect=self.getTrimRect(img, bg)
        return img.copy(rect)

    def getTrimRect(self, img, bg='white'):

        w = img.width();
        h = img.height();
        bg=QtGui.QColor(bg)
        for l in range(w):
            if not self.columnHasBgColor(l, bg, img):
                break
        l = min(l, w / 3);
        for r in range(w-1, l, -1):
            if not self.columnHasBgColor(r, bg, img):
                break
        r = max(r, 2 * w / 3);
        for t in range(h):
            if not self.rowHasBgColor(t, bg, img):
                break
        t = min(t, h / 3);
        for b in range(h - 1, t, -1):
            if not self.rowHasBgColor(b, bg, img):
                break
        b = max(b, 2 * h / 3);
        l = max(l - w / 100, 0);
        t = max(t - h / 100, 0);
        r = min(r + w / 100, w);
        b = min(b + h / 100, h);
        return QtCore.QRect(
                int(float(l) / w),
                int(float(t) / h),
                int(float(r - l) / w),
                int(float(b - t) / h))

    def columnHasBgColor(self, x, bg, img):

        h = img.height()
        for i in range(h):
            pcol=QtGui.QColor(img.pixel(x, i))
            if bg != pcol: return False 
        return True 

    def rowHasBgColor(self, y, bg, img):

        w = img.width();
        for i in range(w):
            pcol=QtGui.QColor(img.pixel(i, y))
            if bg != pcol: return False
        return True 
