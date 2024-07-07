from .view import ViewGo


class WidgetGo(ViewGo):
    def goTo(self, xrange=[1], **kwargs):
        if xrange is None:
            self.goToLast(**kwargs)
        else:
            self.setCurrentRow(xrange[-1] - 1)

    def setCurrentRow(self, row):
        super().setCurrentRow(row)
        self.indexChanged.emit(row + 1)
