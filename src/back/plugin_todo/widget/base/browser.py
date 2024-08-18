from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from PyQt5.QtWebEngineWidgets import *

class BrowserWidget(QWebEngineView):

    hideWanted=pyqtSignal()

    def __init__(self, *args, **kwargs):

        super(BrowserWidget, self).__init__(*args, **kwargs)

        self.html = """
            <!DOCTYPE html>
            <html>
                <head>
                    <title>Title</title>
                    <meta charset="utf-8" />
                </head>
                <body>
                    <p>{}</p>
                </body>
            </html>
            """

        self.page().setBackgroundColor(Qt.transparent)

    def loadHtml(self, html): self.page().setHtml(html)

    def loadCSS(self, path, name='css'):

        path=QFile(path)

        if path.open(QFile.ReadOnly | QFile.Text):

            css = path.readAll().data().decode("utf-8")
            SCRIPT = """
            (function() {
            css = document.createElement('style');
            css.type = 'text/css';
            css.id = "%s";
            document.head.appendChild(css);
            css.innerText = `%s`;
            })()
            """ % (name, css)
            script = QWebEngineScript()
            self.page().runJavaScript(
                    SCRIPT, QWebEngineScript.ApplicationWorld)
            script.setName(name)
            script.setSourceCode(SCRIPT)
            script.setInjectionPoint(QWebEngineScript.DocumentReady)
            script.setRunsOnSubFrames(True)
            script.setWorldId(QWebEngineScript.ApplicationWorld)
            self.page().scripts().insert(script)
