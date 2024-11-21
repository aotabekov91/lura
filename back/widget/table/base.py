from collections import OrderedDict

from PyQt6 import QtCore, QtWidgets

from . import widgets


class TableWidget(QtWidgets.QWidget):
    wmap = {
        "Label": widgets.Label,
        "Image": widgets.Image,
        "LineEdit": widgets.LineEdit,
        "TextEdit": widgets.TextEdit,
    }
    widget_map = {}
    hasWidgets = True
    dataChanged = QtCore.pyqtSignal(object, object)

    def __init__(
        self,
        wmap={},
        space=0,
        hspace=0,
        vspace=0,
        item=None,
        view=None,
        element=None,
        objectName="ItemWidget",
        **kwargs,
    ):
        self.m_view = view
        self.m_item = item
        self.m_space = space
        self.m_element = None
        self.m_vspace = vspace
        self.m_hspace = hspace
        self.m_wmap = wmap.copy()
        self.m_widgets = OrderedDict()
        super().__init__(objectName=objectName, **kwargs)
        self.setupLayout()
        self.setView(view)
        self.setElement(element)

    def element(self):
        return self.m_element

    def setupLayout(self):
        l = QtWidgets.QGridLayout(self)
        self.setLayout(l)
        self.m_layout = l
        l.setSpacing(self.m_space)
        l.setVerticalSpacing(self.m_vspace)
        l.setHorizontalSpacing(self.m_hspace)

    def setView(self, view):
        self.m_view = view
        self.setParent(view)
        if not view:
            return
        view.resized.connect(self.adjustSizeHint)

    def setElement(self, element=None, widgets=None):
        if self.m_element:
            s = getattr(
                self.m_element,
                "dataUpdated",
                None,
            )
            if s:
                s.dataUpdated.disconnect(self.updateData)
            self.delWidgets(self.m_widgets)
        self.m_element = element
        if self.m_element:
            s = getattr(
                self.m_element,
                "dataUpdated",
                None,
            )
            if s:
                s.dataUpdated.connect(self.updateData)
            if not widgets:
                widgets = self.createWidgets()
            self.setWidgets(widgets)

    def createWidgets(
        self,
        element=None,
        widget_map=None,
    ):
        widgets = OrderedDict()
        wmap = widget_map or self.m_wmap
        elem = element or self.m_element
        items = wmap.items()
        data = elem.data()
        for i, (n, d) in enumerate(items):
            klass = d.get("w", "Label")
            p = d.get("p", f"{i}x0x-1x1")
            p = [int(f) for f in p.split("x")]
            t = str(data.get(n, "")).strip()
            t = d.get("t", t)
            pos = (p[0], p[1])
            if type(klass) == str:
                klass = self.wmap.get(klass)
            w = klass(
                data=d,
                text=t,
                index=n,
                parent=self,
                position=pos,
                element=self.m_element,
            )
            oname = n
            widgets[n] = (w, p)
            fname = d.get("n", None)
            if fname:
                fname = fname.split("_")
                d = self.m_element.data()
                ftext = []
                for f in fname:
                    ftext += [d.get(f, "")]
                oname = "_".join(ftext)
            w.setObjectName(oname)
        return widgets

    def delWidgets(self, widgets):
        for w, p in widgets.values():
            self.m_layout.removeWidget(w)
            w.geometryChanged.disconnect(
                self.adjustSizeHint
            )
            w.focusGained.disconnect(self.selectToCenter)
            w.hide()
        self.m_widgets = OrderedDict()

    def setWidgets(self, widgets):
        for w, p in widgets.values():
            self.m_layout.addWidget(w, *p)
            w.focusGained.connect(self.selectToCenter)
            w.geometryChanged.connect(self.adjustSizeHint)
            w.show()
        self.m_widgets = widgets

    def widget(self, key):
        return self.m_widgets.get(key)

    def widgets(self):
        return self.m_widgets

    def updateData(self):
        d = self.m_element.data()
        for n in self.m_widgets.keys():
            self.set(n, str(d[n]).strip())

    def set(self, n, t):
        w, p = self.m_widgets[n]
        w.m_reporting = False
        w.setText(str(t))
        w.m_reporting = True

    def sizeHint(self):
        v = self.size()
        hint = super().sizeHint()
        if not self.m_widgets:
            return hint
        h = 10
        for i, p in self.m_widgets.values():
            h += i.sizeHint().height()
        if self.m_view:
            v = self.m_view.size()
        h = max(hint.height(), h)
        hint.setHeight(h)
        hint.setWidth(v.width())
        return hint

    def adjustSizeHint(self):
        if self.m_item:
            self.m_item.setSizeHint(self.sizeHint())

    def selectToCenter(self):
        if self.m_view:
            self.m_view.setCurrentItem(self.m_item)
            self.m_view.scrollToItem(
                self.m_item, QtWidgets.QAbstractItemView.ScrollHint)
