from PyQt6.QtWidgets import QListWidgetItem

class ListItem(QListWidgetItem):

    def setCurrentItem(self):
        lwidget = self.listWidget()
        lwidget.setCurrentItem(self)

    def setElement(self, e):
        self.m_elem = e
        if hasattr(e, "elementWanted"):
            e.elementWanted.connect(self.setCurrentItem)

    def element(self):
        return self.m_elem
