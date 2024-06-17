from lura.qt import vimo, widget
from lura.qt.mixin import view


class ElementView(
    view.TableWidgetGo,
    view.TableWidgetInput,
    vimo.View,
    widget.TableWidget,
):
    widget_map = {}

    def setup(self):
        self.m_curr = None
        self.m_element_widgets = {}
        super().setup()

    def updateKlass(self):
        super().updateKlass()
        self.m_wmap = self.m_kwargs.get(
            "widget_map", self.widget_map
        )

    def setView(self, view=None):
        self.resized.connect(self.adjustSizeHint)

    def setCurrentIndex(self, row, col):
        for n, (w, p) in self.m_widgets.items():
            if p[0] == row and p[1] == col:
                self.m_curr = [row, col]
                w.setFocus()
                return w

    def resetElement(
        self,
        element,
        widget_map=None,
    ):
        w = self.m_element_widgets.get(element)
        if not w:
            wmap = widget_map or self.m_wmap
            w = self.createWidgets(element, wmap)
            self.m_element_widgets[element] = w
        if element:
            self.setElement(element, w)

    def setFocus(self):
        super().setFocus()
        if self.m_curr:
            self.setCurrentIndex(*self.m_curr)
