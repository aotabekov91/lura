from PyQt5 import QtCore

from .task import SearchTask

class Search:

    canSearch=True
    searchFound=QtCore.pyqtSignal()

    def searchCount(self):
        return len(self.m_search_data)

    def searchCurrentIndex(self):
        return self.m_search_idx

    def setup(self):

        super().setup()
        t=SearchTask()
        p=QtCore.QThreadPool()
        self.m_search_task=t
        self.m_search_pool=p
        self.clearSearchData()
        t.signals.ready.connect(
                self.updateSearchData)
        p.start(t)

    def searchGoTo(self, kind=None, rstart=1):

        d=self.m_search_data
        idx=self.m_search_idx
        if not d: return
        if kind=='first':
            idx=0
        elif kind=='last':
            idx=len(d)-1
        elif kind=='next':
            idx+=1
        elif kind=='prev':
            idx-=1
        elif rstart is None:
            idx=len(d)-1
        else:
            idx=self.m_search_idx+rstart
        if idx>=len(d): 
            idx=0
        elif idx<0: 
            idx=len(d)-1
        self.m_search_idx=idx
        
        self.goTo(path=d[idx])

    def search(self, text):
        self.m_search_task.start(text)

    def updateSearchData(self, data):

        initial=not self.m_search_data and data
        self.m_search_data+=[data]
        m=self.app.ui.moder.mode()
        m.setSubmode('jump')
        self.searchFound.emit()
        if initial: self.searchGoTo()

    def finishSearchMode(self, **kwargs):
        self.clearSearchData()

    def startSearchMode(
            self, text=None, **kwargs):

        self.clearSearchData()
        self.search(text)

    def clearSearchData(self):

        self.m_search_idx=-1
        self.m_search_data=[]
        self.m_search_match=None
        self.m_search_task.stop()
