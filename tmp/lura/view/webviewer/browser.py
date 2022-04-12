from datetime import datetime

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *

from lura.core.widgets.item import ItemWidget
# from .scripts import *

class Page(QWebEnginePage):

    def __init__(self, parent):
        super().__init__(parent)
        self.m_parent=parent
        self.setup()
            
    def parent(self):
        return self.m_parent

    def setup(self):
        pass

    def event(self, event):
        return False

    def keyPressEvent(self, event):
        raise

    def linkHovered(self, url):
        raise

class Browser(QWebEngineView):
    def __init__(self, parent):
        super().__init__(parent)

        self.window=parent.window
        self.setup()

    def page(self):
        return self.m_page

    def setup(self):

        self.setUrl(QUrl('https://google.com'))
        self.selectionChanged.connect(self.on_selectionChanged)

        self.show()
        self.m_page=Page(self)
        self.setPage(self.m_page)

        self.m_layout=QVBoxLayout(self)
        self.createButtons()

        self.m_action=QAction()
        self.m_action.setShortcut(QKeySequence('Ctrl+x'))
        self.addAction(self.m_action)
        self.m_action.triggered.connect(self.activateAnnotation)
        self.m_action.setShortcutContext(Qt.WidgetWithChildrenShortcut)

        self.recogito=open('/home/adam/code/lura/lura/core/webbrowser/recogito.min.js').read()
        self.style=open('/home/adam/code/lura/lura/core/webbrowser/style.py').read()

        # self.annotator=open('/home/adam/code/lura/lura/core/webbrowser/jquery.min.js').read()
        # self.page().runJavaScript(self.annotator)

        # self.annotator=open('/home/adam/code/lura/lura/core/webbrowser/annotator.min.js').read()
        # self.page().runJavaScript(self.annotator)

        # html=open('/home/adam/code/lura/lura/core/webbrowser/demo.html').read()
        # self.page().setHtml(html)

        # script='var app = new annotator.App(); app.include(annotator.ui.main); app.start();'
        # self.page().runJavaScript(script)

        # self.annotator=open('/home/adam/code/lura/lura/core/webbrowser/annotator.min.js').read()
        # self.page().runJavaScript(self.annotator)

                # '(function() {var app = new annotator.App(); app.include(annotator.ui.main); app.start();})()')
        # self.page().runJavaScript('var r = Recogito.init({content: document.body })')

        self.annotationActivated=False

    def contextMenuEvent(self, event):
        raise

    def event(self, event):
        print(self.__class__.__name__)
        return False

    def activateAnnotation(self):

        if not self.annotationActivated:

            self.annotator=open('/home/adam/code/lura/lura/core/webbrowser/annotator.min.js').read()
            self.page().runJavaScript(self.annotator)

            script='''
                var app = new annotator.App(); 
                app.include(annotator.ui.main, {
                    editorExtensions: [annotator.ui.tags.editorExtension],
                    viewerExtensions: [annotator.ui.tags.viewerExtension]
                });
                app.include(annotator.storage.http, {
                    prefix: 'http://127.0.0.1:5000'
                });

                app.start();
                '''

            self.page().runJavaScript(script)

            self.annotationActivated=True

        else:

            # self.page().runJavaScript('(function() {var r = Recogito.destroy()})();')

            self.annotationActivated=False

    def mouseReleaseEvent(self, event):
        raise

    def eventFilter(self, m_object, event):
        raise
    
    def close(self):
        self.window.close()

    def addAnnotation(self):

        self.page().runJavaScript(scR)

    def toggleActionsMenu(self):
        if self.actionsMenu.isVisible():
            self.actionsMenu.hide()
            self.setFocus()
        else:
            self.actionsMenu.show()
            self.actionsMenu.setFocus()

    def createButtons(self):
        navbar = QToolBar()

        # Goback button
        back_button = QAction('Backward',self)
        back_button.triggered.connect(self.back)
        navbar.addAction(back_button)

        #forward button
        forward_button = QAction('Forward',self)
        forward_button.triggered.connect(self.forward)
        navbar.addAction(forward_button)

        #activate navBar
        self.url_bar = QLineEdit(self)
        self.url_bar.returnPressed.connect(self.navigation)
        self.urlChanged.connect(self.update_url)

        self.m_layout.addWidget(navbar)
        self.m_layout.addWidget(self.url_bar)
        self.m_layout.addWidget(self)


    def saveAsPdf(self):


        title=self.title().replace(' ', '_')
        url=self.url().toString(QUrl.RemovePassword|QUrl.RemoveUserInfo)
        domain=self.url().toString(QUrl.RemoveScheme|QUrl.RemoveQuery|QUrl.RemoveFragment)
        domain=domain.replace('/', '_')

        filePath='/home/adam/docs/docs/websites/{}.pdf'
        from pathlib import Path

        filePath=filePath.format(f'{title}_{domain}')
        Path(filePath).touch(exist_ok=True)

        self.page().printToPdf(filePath)
        self.page().pdfPrintingFinished.connect(self.on_pdfPrintingFinished)

    def on_pdfPrintingFinished(self, filePath, success):

        if success:

            document=self.window.buffer.loadDocument(filePath)

            title=self.title().replace(' ', '_')
            url=self.url().toString(QUrl.RemovePassword|QUrl.RemoveUserInfo)

            self.window.plugin.metadata.db.setTitle(document, title) 
            self.window.plugin.metadata.db.setUrl(document, url)
            self.window.plugin.metadata.db.setKind(document, 'website')
            timestamp = datetime.timestamp(datetime.now())
            self.window.plugin.metadata.db.setAccessTime(document, timestamp)

            self.window.open(filePath)

    def bookmark(self):
        self.toggleActionsMenu()

        # bookmark={'position': self.browser.url(),
        #         'text': self.browser.title()}
        # print(bookmark)

    def navigation(self):
        url = self.url_bar.text()
        if not 'https://' in url: url='https://'+url
        self.setUrl(QUrl(url))

    def update_url(self,arg):
        self.url_bar.setText(arg.toString())

    def on_selectionChanged(self):
        pass

    def mouseMoveEvent(self, event):
        raise

    def eventFilter(self, m_object, event):
        print('a')
        if event.type()==Qt.MouseEvent: 
            pass

