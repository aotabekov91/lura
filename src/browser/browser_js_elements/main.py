import os
import pathlib

from plug import Plug

class BrowserJSElements(Plug):

    views=['BrowserView']

    def setup(self):
        super().setup()
        self.loadJSCode()
        self.app.buffman.viewCreated.connect(
                self.injectJSCode)

    def loadJSCode(self):
        script="""
        (function() {
            "use strict";
            if (!window.hasOwnProperty("_qutebrowser")) {
                window._qutebrowser = {"initialized": {}};
            }
            if (window._qutebrowser.initialized["{{name}}"]) {
                return;
            }
            %s
            window._qutebrowser.initialized["%s"] = true;
        })();
        """
        file=self.files.get('elements.js', None)
        if file and os.path.exists(file):
            path=pathlib.Path(file)
            js_code=path.read_text(encoding='utf-8')
            self.m_code=script%(js_code, 'scripts')

    def isCompatible(self, view):
        if view:
            for klass in view.__class__.__mro__:
                if klass.__name__ in self.views:
                    return True
        return False

    def injectJSCode(self, view):
        if self.m_code and self.isCompatible(view):
            view.injectJSCode('elements', self.m_code, subframes=True)
