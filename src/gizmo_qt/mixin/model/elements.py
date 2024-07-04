from PyQt6 import QtCore


class Elements:
    hasElements = True
    loaded = QtCore.pyqtSignal(object)
    elementCreated = QtCore.pyqtSignal(object)

    def count(self):
        return len(self.m_elements)

    def elements(self):
        if not self.m_loaded:
            self.load()
        return self.m_elements

    def element(self, idx):
        return self.m_elements.get(idx, None)

    def sourceElement(self):
        for i, e in self.m_elements.items():
            if e.data() == self.m_source:
                return e

    def load(self):
        if self.element_class:
            elems = {}
            for i, d in enumerate(self.m_data):
                e = self.element_class(
                    data=d,
                    index=i + 1,
                    model=self,
                )
                elems[i + 1] = e
                self.elementCreated.emit(e)
            self.m_elements = elems
            self.loaded.emit(self)
