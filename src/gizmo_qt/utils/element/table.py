from PyQt6 import QtCore

import plug


class TableElement(
    plug.Element,
    QtCore.QObject,
):
    m_item = None
    m_litem = None
    m_widget = None

    def setWidget(self, w):
        self.m_widget = w
        s = getattr(w, "widgetDataChanged", None)
        if s and self.m_model:
            m = self.m_model
            s.connect(m.widgetDataChanged)

    def widget(self):
        return self.m_widget

    def setItem(self, item):
        self.m_item = item
        item.setElement(self)

    def item(self):
        return self.m_item

    def setListItem(self, item):
        self.m_litem = item

    def listItem(self):
        return self.m_litem
