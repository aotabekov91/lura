from PyQt6 import QtWebEngineWidgets, QtWidgets, QtCore

from plug_qt import vimo

class BrowserView(vimo.View, QtWidgets.QFrame):

    def setup(self):
        super().setup()
        self.setupBrowser()

    def browser(self):
        return self.m_browser

    def page(self):
        return self.m_browser.page()

    def setupBrowser(self):
        self.m_browser=QtWebEngineWidgets.QWebEngineView()
        self.m_browser.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground)
        self.m_layout=QtWidgets.QHBoxLayout(self)
        self.m_layout.setContentsMargins(0, 0, 0, 0)
        self.m_layout.setSpacing(0)
        self.setLayout(self.m_layout)
        self.m_layout.addWidget(self.m_browser)

    @classmethod
    def assemble(cls, module, function, *args) -> str:
        js_args = ', '.join(cls.toJS(arg) for arg in args)
        if module == 'window':
            parts = ['window', function]
            code = '"use strict";\n{}({});'.format('.'.join(parts), js_args)
            return code

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
            raise TypeError("Don't know how to handle {!r} of type {}!".format(
                arg, type(arg).__name__))

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
        for text, rep in replacements:
            text = text.replace(text, rep)
        return text
