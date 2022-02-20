import time
from datetime import datetime

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebChannel import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *

from .js.scripts import *
from ..page import WebPage
from ..annotation import WebAnnotation

from lura.render.base import Document
from .js.connector import JSConnector

scripts='/home/adam/code/lura/lura/render/web/document/js'

class WebDocument(Document):


    loadFinished=pyqtSignal(bool)

    def __init__(self, url):
        super().__init__(self.getPurifiedUrl(url))
        self.m_shouldRegister=False
        self.m_page=WebPage(self)
        self.setup()

    def page(self):
        return self.m_page

    def id(self):
        if self.m_id is None: self.register()
        return self.m_id

    def register(self):
        self.m_shouldRegister=True
        self.window.documentCreated.emit(self)
        self.setTitle(self.m_page.title())
        self.setKind('website')

    def document(self):
        return self

    def setParent(self, window):
        super().setParent(window)
        self.window=window

    def annotations(self):
        if not self.loadStatus: return []
        return self.window.plugin.annotation.getBy({'field': 'did', 'value':self.m_id})

    def annotate(self, data):
        if not self.registered(): self.register()
        annotation=WebAnnotation()
        annotation.setAnnotationData(data)
        annotation.setPage(self.m_page)
        self.m_annotations+=[annotation]
        self.window.annotationCreated.emit(annotation)

    def embeddedTitle(self):
        return self.m_page.title()

    def embeddedAuthor(self):
        return ''
        
    def getPurifiedUrl(self, url=None):
        if url is None: url=self.url().toString()
        return QUrl(url).toString(QUrl.RemovePassword|QUrl.RemoveUserInfo)

    def load(self, page=0, left=0, top=0):
        self.m_page.setUrl(QUrl(self.m_filePath))

    def shouldRegister(self):
        return self.m_shouldRegister

    def isOnline(self):
        return True

    def readSuccess(self):
        return True

    def setup(self):

        self.loadStatus=False
        self.annotationActivated=False

        self.db= JSConnector(self)
        self.db.jsAnnotationCreated.connect(self.on_annotationCreated)
        self.channel = QWebChannel(self)
        self.channel.registerObject("db", self.db)

        self.m_page.loadFinished.connect(self.on_loadFinished)
        self.m_page.loadFinished.connect(self.loadFinished)

    def on_annotationCreated(self, data):
        if not self.registered(): self.setId(data['did'].toInt())
        f=self.window.plugin.annotation
        annotation=f.get(data['id'].toInt())
        self.m_annotations+=[annotation]
        self.annotationAdded.emit(annotation)

    def on_loadFinished(self, success):
        if not success: return 

        self.page().runJavaScript(open(f'{scripts}/qwebchannel.js').read())
        self.page().runJavaScript(open(f'{scripts}/jquery.min.js').read())
        self.page().runJavaScript(open(f'{scripts}/unminified.annotator.js').read())

        self.page().setWebChannel(self.channel)
        self.page().runJavaScript(channelActivatorScript)
        self.page().runJavaScript(annotatorScript)

        self.page().runJavaScript(loadScript)
        self.loadStatus=True
        # self.loadAnnotations()

    def jumpToPage(self, pageNumber, left, top):
        self.page().runJavaScript(f"window.scrollTo({left},{top});")

    def saveLeftAndTop(self):
        point=self.m_page.scrollPosition()
        return point.x(), point.y()

    def fitToPageWidth(self):
        self.page().runJavaScript("db.width(document.documentElement.scrollWidth);")
        left, top=self.saveLeftAndTop()
        self.jumpToPage(0, left, top-100)

    def on_fitToPageWidth(self, m_width=None):
        if m_width in [None, 0]: return
        self.page().setZoomFactor(self.browser.width()/m_width)

    def color(self):
        if not hasattr(self, 'm_color'): return QColor('#fcfcf2')
        return self.m_color

    def setColor(self, color):
        self.m_color=color
