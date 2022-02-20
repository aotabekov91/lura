from datetime import datetime

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *

from lura.render.web import WebDocument

class BrowserView(QWidget):
    def __init__(self, parent, settings):
        super(QWidget,self).__init__(parent)

        self.window=parent
        self.s_settings=settings['BrowserView']

    def updateUrl(self, url=None):

        if url is None: 
            url=self.url_bar.text()
        else:
            url=url.toString()

        if not 'https://' in url: url='https://'+url
        self.window.open(url)

    def open(self, document, page=0, left=0, top=0):

        self.m_browser=MQWebEngineView(self)
        self.m_layout=QVBoxLayout(self)

        self.m_document=document
        self.m_document.browser=self.m_browser

        self.m_browser.setPage(document.page())

        self.m_document.loadFinished.connect(lambda: self.m_document.jumpToPage(page, left, top))
        self.m_document.load()
        self.m_browser.show()

        self.createButtons()
        self.createActionMenu()

        self.url_bar.setText(document.filePath())
        self.m_browser.urlChanged.connect(self.updateUrl)

    def fitToPageSize(self):
        pass

    def readjust(self):
        pass
        # self.m_document.load()

    def document(self):
        return self.m_document

    def close(self):
        self.window.close()

    def createActionMenu(self):

        self.actionsMenu=QListWidget(self)
        self.actionsMenu.setFixedHeight(200)

        self.actionsMenu.setMinimumWidth(self.actionsMenu.sizeHintForRow(0))
        self.m_layout.addWidget(self.actionsMenu)

        self.actionsMenu.hide()

        self.m_menuAction=QAction()
        self.m_menuAction.setShortcut(self.s_settings['shortcuts']['toggleActionsMenu'])
        self.m_menuAction.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.addAction(self.m_menuAction)
        self.m_menuAction.triggered.connect(self.toggleActionsMenu)

        self.setActions()

    def setActions(self):
        self.m_actions=[]
        for func, key in self.s_settings['BrowserMenu'].items():
            m_action=QAction(f'({key}) {func}')
            m_action.setShortcut(QKeySequence(key))
            m_action.setShortcutContext(Qt.WidgetShortcut)
            self.m_actions+=[m_action]
            m_action.triggered.connect(getattr(self, func))
            self.actionsMenu.addAction(m_action)
            self.actionsMenu.addItem(m_action.text())

        m_action=QAction()
        m_action.setShortcut(Qt.Key_Escape)
        m_action.setShortcutContext(Qt.WidgetShortcut)
        self.m_actions+=[m_action]
        m_action.triggered.connect(self.actionsMenu.hide)
        self.actionsMenu.addAction(m_action)

    def toggleActionsMenu(self):
        if self.actionsMenu.isVisible():
            self.actionsMenu.hide()
            self.setFocus()
        else:
            self.actionsMenu.show()
            self.actionsMenu.setFocus()

    def toggleNavigation(self):
        self.toggleActionsMenu()
        if self.navbar.isVisible():
            self.navbar.hide()
        else:
            self.navbar.show()

    def createButtons(self):
        self.navbar = QToolBar()

        back_button = QAction('<',self)
        back_button.setShortcut(QKeySequence('Shift+h'))

        back_button.triggered.connect(self.m_browser.back)
        self.navbar.addAction(back_button)

        forward_button = QAction('>',self)
        forward_button.setShortcut(QKeySequence('Shift+l'))
        forward_button.triggered.connect(self.m_browser.forward)
        self.navbar.addAction(forward_button)

        self.url_bar = QLineEdit(self)
        self.url_bar.returnPressed.connect(self.updateUrl)
        self.navbar.addWidget(self.url_bar)

        self.m_layout.addWidget(self.navbar)
        self.m_layout.addWidget(self.m_browser)

    def fitToPageWidth(self):
        left, top=self.saveLeftAndTop()
        self.jumpToPage(0, left, top)

    def jumpToPage(self, pageNumber=0, left=0, top=0):
        self.m_document.jumpToPage(pageNumber, left, top)

    def currentPage(self):
        return 0

    def saveLeftAndTop(self):
        return self.m_document.saveLeftAndTop()

    def pageUp(self):
        left, top=self.saveLeftAndTop()
        self.jumpToPage(0, left, top-100)

    def pageDown(self):
        left, top=self.saveLeftAndTop()
        self.jumpToPage(0, left, top+100)

    def keyPressEvent(self, event):
        if event.key()==Qt.Key_J:
            self.pageDown()
        elif event.key()==Qt.Key_K:
            self.pageUp()

    def totalPages(self):
        return 1

    def save(self):
        pass


class MQWebEngineView(QWebEngineView):

    def resizeEvent(self, event):
        self.parent().m_document.fitToPageWidth()

    def event(self, event):
        if event.type()==QEvent.Enter: self.parent().window.setView(self.parent())
        return super().event(event)
