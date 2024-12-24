import os

from PyQt6 import QtWebEngineCore

from plug import Plug, tag

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
            self.setViewCSS(view)

    def setDefaultStyles(self):
        styles=self.files.get('styles', None)
        if styles:
            for style in os.listdir(styles):
                path=os.path.join(styles, style)
                name=style.replace('.css', '')
                with open(path, 'r') as file:
                    css=file.read()
                    data=self.app.styleman.cssToDict(css)
                    self.m_styles[name]=self.app.styleman.dictToCSS(data)
            self.setStyleFiller()

    def setDefaultCSS(self):
        self.m_style=self.default_style
        self.m_css=self.m_styles.get(self.m_style)

    def setStyleCSS(self):
        self.m_css=self.setDefaultCSS()
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
                self.m_css=self.m_css

    def setStyleFiller(self) -> None:
        styles = self.m_styles.keys()
        filler={'style': list(styles)}
        self.app.buffman.addFiller(
                "stylehelp", filler)

    def setViewCSS(self, view):
        css_script = """
        (function() {
        css = document.createElement('style');
        css.type = 'text/css';
        document.head.appendChild(css);
        css.innerText = '%s';
        })()""" %(self.m_css)
        browser=view.browser()
        page=browser.page()
        klass=QtWebEngineCore.QWebEngineScript
        script = klass() 
        script.setName(self.name)
        script.setSourceCode(css_script)
        script.setInjectionPoint(
                klass.InjectionPoint.DocumentReady)
        script.setRunsOnSubFrames(True)
        script.setWorldId(klass.ScriptWorldId.ApplicationWorld)
        page.scripts().insert(script)

    @tag('(exec)')
    def stylehelp(self, style):
        self.m_css=self.m_styles.get(style, self.m_css)
