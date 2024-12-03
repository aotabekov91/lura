class Annotate:
    canAnnotate = True

    def setElement(self, e):
        super().setElement(e)
        e.dataUpdated.connect(self.update)
