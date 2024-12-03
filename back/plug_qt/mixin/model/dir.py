import os


class Dir:
    def assignId(self):
        if os.path.exists(self.m_source):
            f = os.path.dirname(self.m_source)
            self.m_folder = f

    def load(self):
        self.m_folder = None
        self.m_data = {}
        self.assignId()
        self.setFiles()
        super().load()

    def setFiles(self):
        if self.m_folder:
            idx = 0
            for f in os.listdir(self.m_folder):
                c = self.isCompatible(f)
                if not c:
                    continue
                idx += 1
                p = os.path.join(self.m_folder, f)
                self.m_data[idx] = p

    def sourceElement(self):
        return self.m_elements.get(self.m_source, None)

    def jumpToSource(self):
        e = self.sourceElement()
        for i, j in self.m_items.items():
            if j.element() == e:
                return self.goTo(i)
