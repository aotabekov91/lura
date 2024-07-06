from plug_qt.utils import miscel


class SearchTask(miscel.Task):
    def setup(self):
        super().setup()
        self.m_model = self.kwargs.get("model")
        self.m_model.searchFound

    def start(self, text):
        raise

    def run(self):
        for i, e in self.m_elements.items():
            f = e.search(text)
            if f:
                self.searchFound.emit(e, f)
