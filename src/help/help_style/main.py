from PyQt6 import QtWebEngineCore
from PyQt6 import QtWebEngineWidgets

from plug import Plug

class HelpStyle(Plug):

    default_style='github'

    def setup(self):
        super().setup()
        self.m_css=None
        self.m_styles={}
        self.m_style=None
        self.setDefaultStyles()
        self.app.buffman.viewCreated.connect(
                self.checkView)
        if self.app.running:
            self.setStyleCSS()
        else:
            self.app.appSoonStarts.connect(
                    self.setStyleCSS)

    def checkView(self, view):
        if view.name=='HelpView':
            raise

    def setDefaultStyles(self):
        pass

    def setDefaultCSS(self):
        self.m_style=self.default_style
        self.m_css=self.m_styles.get(self.m_style)

    def setStyleCSS(self):
        style=self.app.styleman.style()
        if style:
            data, _ = style
            helpview_data={}
            for key, value in data.items():
                if key.startswith('#HelpView'):
                    key=key.replace('#HelpView', '')
                    helpview_data[key]=value
            if helpview_data:
                self.m_style=style
                self.m_css=self.app.styleman.dictToCSS(helpview_data)
                return self.m_css
        return self.setDefaultCSS()

    def loadCSS(self, view):
        css_script = """
        (function() {
        css = document.createElement('style');
        css.type = 'text/css';
        css.id = {name};
        document.head.appendChild(css);
        css.innerText = {css};
        })()
        """.format(name=self.m_style, css=self.m_css)
        page=view.page()
        klass=QtWebEngineCore.QWebEngineScript
        script = klass() 
        page.runJavaScript(
                script, klass.ScriptWorldId.ApplicationWorld)
        script.setName(self.name)
        script.setSourceCode(css_script)
        script.setInjectionPoint(
                klass.InjectionPoint.DocumentReady)
        script.setRunsOnSubFrames(True)
        script.setWorldId(klass.ScriptWorldId.ApplicationWorld)
        page.scripts().insert(script)
