import time

from PyQt6 import QtCore


class Signals(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    created = QtCore.pyqtSignal(object)


class Runner(QtCore.QRunnable):
    def __init__(
        self,
        view,
        config={},
        klass=None,
        model=None,
        scaleFactor=1,
    ):
        self.force = False
        self.m_view = view
        self.m_model = model
        self.m_klass = klass
        self.m_config = config
        self.m_sfactor = scaleFactor
        self.signals = Signals()
        super().__init__()
        self.m_model.elementCreated.connect(self.createItem)
        self.m_model.loaded.connect(self.setLastIndex)

    def setLastIndex(self):
        self.m_last = self.m_model.count()

    @QtCore.pyqtSlot()
    def run(self):
        if self.m_klass and self.m_model:
            self.m_index = 0
            self.m_last = None
            self.m_model.load()
            while not self.checkFinished():
                time.sleep(0.01)
        self.signals.finished.emit()

    def checkFinished(self):
        return self.m_index == self.m_last

    def createItem(self, e):
        self.m_index += 1
        i = self.m_klass(
            element=e,
            index=self.m_index,
            config=self.m_config,
            scaleFactor=self.m_sfactor,
        )
        self.signals.created.emit(i)
