import os
import re
import collections
import typing as tp

from ..plug import Plug
from ..utils import tag

class Styleman(Plug):

    current: str = None
    style: str = "default"
    styles: tp.Dict[str, tp.Any] = {}

    def setup(self):
        super().setup()
        self.setColorschemeFiller()

    def setColorschemeFiller(self) -> None:
        self.app.buffman.setFiller(
            "colorscheme", self.colorschemeFiller)

    def colorschemeFiller(self, name) -> tp.List[str]:
        alist = []
        keys = self.styles.keys()
        if not name:
            return keys
        for n in keys:
            l = len(name)
            if n[:l] == name:
                alist += [n]
        return alist

    def cssToDict(self, css) -> tp.Dict[str, str]:
        settings = {}
        css = css.strip()
        css = re.sub(r"[\n\t]", " ", css)
        css = re.sub("}", "}__::__", css)
        pattern = r"([^{]*){([^}]*)}"
        tmp = css.split("__::__")
        for text in tmp:
            if not text:
                continue
            text = text.strip()
            m = re.match(pattern, text)
            if m:
                name = m.group(1).strip()
                inside = m.group(2).strip()
                m = {}
                for i in inside.split(";"):
                    if i:
                        i = i.strip()
                        j = i.split(":", 1)
                        m[j[0].strip()] = j[1].strip()
                settings[name] = m
        return settings

    def dictToCSS(
        self,
        style: tp.Dict[str, str],
    ) -> str:
        parts = []
        for k, v in style.items():
            inside = []
            for i, j in v.items():
                inside += [f" {i}: {j}"]
            inside = "; ".join(inside) + "; }"
            parts += [k + " {" + f" {inside} "]
        css = " ".join(parts)
        return css

    def updateDefault(self) -> None:
        self.setDefault(self.app.plugman.plugs)
        self.colorscheme(self.style)

    def updateColorscheme(
        self,
        css: str,
    ) -> tp.Dict[str, str]:
        ddict, dcss = self.styles.get("default")
        tmp = ddict.copy()
        return self.updateStyle(tmp, css)

    def updateStyle(
        self,
        base: tp.Dict[str, str],
        append: tp.Dict[str, str],
    ) -> tp.Dict[str, str]:
        for n, a in append.items():
            v = base.pop(n, {})
            v.update(a)
            base[n] = v
        return base

    def setDefault(self, plugs):
        # todo model_view css rewrites default
        default = collections.OrderedDict()
        for name, plug in plugs.items():
            if hasattr(plug, "ui"):
                style = plug.ui.styleSheet()
                if style:
                    style = self.cssToDict(style)
                    self.updateStyle(default, style)
            file = plug.files.get("style.css", None)
            if file:
                style = self.read(file)
                self.updateStyle(default, style)
        file = self.app.files.get("style.css", None)
        if file:
            style = self.read(file)
            self.updateStyle(default, style)
        css = self.dictToCSS(default)
        self.styles["default"] = (default, css)

    def read(
        self,
        path: str,
    ) -> tp.Union[None, tp.Dict[str, str]]:
        if not os.path.exists(path):
            return
        with open(path, "r") as y:
            lines = " ".join(y.readlines())
            css = re.sub(r"[\n\t]", " ", lines)
            return self.cssToDict(css)

    def addColorscheme(
        self, name: str, css: str, update: bool = True
    ) -> None:
        if update:
            css = self.updateColorscheme(css)
        css = self.dictToCSS(css)
        self.styles[name] = (css, css)
        self.reloadColorscheme()

    def reloadColorscheme(self) -> None:
        if self.current != self.style:
            self.colorscheme(self.style)

    @tag("(exec)", filler={"colorscheme": "colorscheme"})
    def colorscheme(self, colorscheme: str) -> None:
        style = self.styles.get(colorscheme, None)
        default = self.styles.get("default", None)
        if style:
            cdict, css = style
            self.current = self.style = colorscheme
            if default:
                _, dcss = default
                css = dcss + css
            self.app.qapp.setStyleSheet(css)
        elif default:
            _, css = default
            self.app.qapp.setStyleSheet(css)
            self.current = "default"
        else:
            self.current = None
