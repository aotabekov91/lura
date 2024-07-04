from PyQt6 import QtCore, QtGui

from .utils import BaseCursor


class CursorMixin:
    cursor_class = BaseCursor
    todo

    def __init__(
        self,
        cache={},
        items={},
        app=None,
        config={},
        scene=None,
        model=None,
        index=None,
        selected=[],
        parent=None,
        cursor=None,
        scaleFactor=1.0,
        objectName="View",
        zoomFactor=0.1,
        continuousView=False,
        scaleMode="FitToWindowHeight",  # Todo a bug
        scene_bcolor=QtGui.QColor("black"),
        **kwargs,
    ):
        self.app = app
        self.m_cut = []
        self.m_yanked = []
        self.m_elements = {}
        self.m_curr = None
        self.m_prev = None
        self.m_id = (index,)
        self.m_cache = cache
        self.m_scene = scene
        self.m_items = items
        self.m_model = model
        self.m_cursor = cursor
        self.m_config = config
        self.scaleMode = scaleMode
        self.m_selected = selected
        self.scaleFactor = scaleFactor
        self.scene_bcolor = scene_bcolor
        self.continuousView = continuousView
        self.zoomFactor = zoomFactor
        super().__init__(parent=parent)
        self.setup()
        self.initialize()

    def setCurrentItem(self, *args, **kwargs):
        pass

    def refresh(self):
        pass

    def update(self, refresh=False):
        pass

    def updateAll(self, refresh=False):
        pass

    def increment(self, *args, **kwargs):
        pass

    def derement(self, *args, **kwargs):
        pass

    def open(self, *arg, **kwargs):
        pass

    def goToEnd(self):
        pass

    def goToBegin(self):
        pass

    def save(self, *args, **kwargs):
        pass

    def cleanUp(self, *args, **kwargs):
        pass

    def paint(self, *args, **kwargs):
        pass

    def setupView(self, *args, **kwargs):
        pass

    def setupItems(self, *args, **kwargs):
        pass

    def setItems(self, *args, **kwargs):
        pass

    def getLocation(self, encode=True):
        pass

    def isDifferentPos(self, *args, **kwargs):
        pass

    def kind(self):
        if self.m_model:
            return self.m_model.kind

    def setSettings(self):
        c = self.m_config
        for k, v in c.items():
            setattr(self, k, v)

    def setup(self):
        self.setSettings()
        self.setupLayout()
        self.setupView()
        self.setupCursor()
        self.setupScene()
        self.setupConnect()
        self.setupScrollBars()

    def setId(self, vid):
        self.m_id = vid

    def id(self):
        return self.m_id

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resized.emit(self, event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.mouseMoveOccured.emit(self, event)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.mousePressOccured.emit(self, event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.mouseReleaseOccured.emit(self, event)

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        self.mouseDoubleClickOccured.emit(self, event)
