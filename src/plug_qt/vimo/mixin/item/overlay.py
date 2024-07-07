from PyQt6 import QtCore, QtWidgets


class Overlay:
    canOverlay = True

    def showOverlay(
        self,
        overlay,
        hideOverlay,
        elements,
        selectedElement,
    ):
        for e in elements:
            if not e in overlay:
                self.addProxy(overlay, hideOverlay, e)
            if e == selectedElement:
                overlay[e].widget().setFocus()

    def hideOverlay(self, overlay, deleteLater=False):
        dover = Overlay()
        dover.swap(overlay)
        if not dover.isEmpty():
            for i in range(dover.constEnd()):
                if deleteLater:
                    raise
            self.refresh()

    def addProxy(
        self,
        position,
        widget,
        hideOverlay,
    ):
        proxy = QtWidgets.QGraphicsProxyWidget(self)
        proxy.setWidget(widget)
        widget.setFocus()
        proxy.setAutoFillBackground(True)
        self.setProxyGeometry(position, proxy)
        proxy.visibleChanged.connect(hideOverlay)
        return proxy

    def setProxyGeometry(self, pos, proxy):
        w = proxy.preferredWidth()
        h = proxy.preferredHeight()
        x = pos.x() - 0.5 * proxy.preferredWidth()
        y = pos.y() - 0.5 * proxy.preferredHeight()
        x = max([x, self.m_brect.left()])
        y = max([y, self.m_brect.top()])
        w = min([w, self.m_brect.right() - x])
        h = min([h, self.m_brect.bottom() - y])
        proxy.setGeometry(QtCore.QRectF(x, y, w, h))
