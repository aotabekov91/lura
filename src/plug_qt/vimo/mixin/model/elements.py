from PyQt6 import QtCore

class Elements:

    hasElements = True
    loaded = QtCore.pyqtSignal(object)
    elementCreated = QtCore.pyqtSignal(object)

    def elements(self):
        if not self.m_loaded:
            self.load()
        return self.m_elements

    def sourceElement(self):
        for i, e in self.m_elements.items():
            if e.data() == self.m_source:
                return e

    def load(self):
        if self.element_class:
            elements = {}
            for idx, data in enumerate(self.m_data):
                element = self.element_class(
                    data=data,
                    index=idx + 1,
                    model=self,
                )
                elements[idx + 1] = element
                self.elementCreated.emit(element)
            self.m_elements = elements
            self.loaded.emit(self)
