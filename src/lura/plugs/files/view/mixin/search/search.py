from gizmo import mixin

from .task import SearchTask

class Search(mixin.view.Search):

    def setupSearchTask(
            self, task=None):

        super().setupSearchTask(SearchTask)

    def searchSetCurrentIndex(self, idx):

        item=self.searchGetItem(idx)
        self.goTo(path=item)
        super().searchSetCurrentIndex(idx)
