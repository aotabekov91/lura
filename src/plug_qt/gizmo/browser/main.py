from PyQt6.QtWebEngineCore import QWebEngineScript
from PyQt6 import QtWebEngineWidgets, QtWidgets, QtCore, QtGui

from plug_qt import vimo

class BrowserView(vimo.View, QtWidgets.QFrame):

    def setup(self):
        super().setup()
        self.m_trans = QtGui.QTransform()
        self.setupBrowser()

    def updateTransformation(self, size):
        self.m_trans.reset()
        self.m_trans.scale(size.width(), size.height())

    def unify(self, polygon):
        #todo
        raise

    def unity(self, polygon):
        # todo
        raise

    def mapToView(self, polygon):
        polygon = self.getPolygon(polygon)
        if unified:
            polygon = self.m_element.unity(polygon)
        if type(polygon) in [
            QtCore.QPoint,
            QtCore.QPointF,
        ]:
            return self.m_trans.map(polygon)
        else:
            return self.m_trans.mapRect(polygon)

    def getPolygon(self, polygon):
        if type(polygon) == tuple:
            if len(polygon) == 2:
                return QtCore.QPointF(*polygon)
            elif len(polygon) == 4:
                polygon = QtCore.QRectF(*polygon)
                return polygon.normalized()
        return polygon

    def browser(self):
        return self.m_browser

    def page(self):
        return self.m_browser.page()

    def setupBrowser(self):
        self.m_browser=QtWebEngineWidgets.QWebEngineView()
        self.m_browser.setAttribute(
                QtCore.Qt.WidgetAttribute.WA_StyledBackground)
        self.setAttribute(
                QtCore.Qt.WidgetAttribute.WA_StyledBackground)
        self.m_layout=QtWidgets.QHBoxLayout(self)
        self.m_layout.setContentsMargins(0, 0, 0, 0)
        self.m_layout.setSpacing(0)
        self.setLayout(self.m_layout)
        self.m_layout.addWidget(self.m_browser)
        page=self.m_browser.page()
        page.contentsSizeChanged.connect(self.updateTransformation)

    @classmethod
    def assemble(cls, module, function, *args) -> str:
        js_args = ', '.join(cls.toJS(arg) for arg in args)
        if module=='':
            return '"use strict";\n{}({});'.format(
                    function, js_args)
        elif module == 'window':
            parts = ['window', function]
        else:
            parts = ['window', '_qutebrowser', module, function]
        return '"use strict";\n{}({});'.format(
                '.'.join(parts), js_args)

    @classmethod
    def toJS(cls, arg) -> str:
        if arg is None:
            return 'undefined'
        elif isinstance(arg, str):
            return '"{}"'.format(cls.escapeString(arg))
        elif isinstance(arg, bool):
            return str(arg).lower()
        elif isinstance(arg, (int, float)):
            return str(arg)
        elif isinstance(arg, list):
            return '[{}]'.format(', '.join(cls.toJS(e) for e in arg))
        else:
            msg="Don't know how to handle {!r} of type {}!"
            raise TypeError(msg.format(arg, type(arg).__name__))

    @classmethod
    def escapeString(cls, text: str) -> str:
        replacements = (
            ('\\', r'\\'),  # First escape all literal \ signs as \\.
            ("'", r"\'"),   # Then escape ' and " as \' and \".
            ('"', r'\"'),   # (note it won't hurt when we escape the wrong one).
            ('\n', r'\n'),  # We also need to escape newlines for some reason.
            ('\r', r'\r'),
            ('\x00', r'\x00'),
            ('\ufeff', r'\ufeff'),
            ('\u2028', r'\u2028'),
            ('\u2029', r'\u2029'),
        )
        for match, rep in replacements:
            text = text.replace(match, rep)
        return text

    def injectJSCode(
            self, 
            name, 
            code, *, 
            subframes=False,
            world=QWebEngineScript.ScriptWorldId.ApplicationWorld, 
            injection_point=QWebEngineScript.InjectionPoint.DocumentCreation, 
            ):
        script = QWebEngineScript()
        script.setInjectionPoint(injection_point)
        script.setSourceCode(code)
        script.setWorldId(world)
        script.setRunsOnSubFrames(subframes)
        script.setName(f'browserview_{name}')
        self.page().scripts().insert(script)

    def runJSCode(
            self, 
            *args, 
            world=QWebEngineScript.ScriptWorldId.ApplicationWorld, 
            **kwargs):
        return self.page().runJavaScript(*args, worldId=world, **kwargs)
