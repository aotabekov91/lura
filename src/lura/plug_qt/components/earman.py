import typing as tp
from PyQt6 import QtCore, QtGui

from lura.gizmo.ui.core import components

# todos
# non-blocking pure python timer
# pure python standard events

mapping = {
    16777220: "<return>",
    0x2F: "/",
    0x01000000: "<escape>",
    0x01000001: "<tab>",
    0x01000002: "<backtab>",
    0x01000003: "<backspace>",
    0x01000004: "<return>",
    0x01000005: "<return>",
    0x01000006: "<insert>",
    0x01000007: "<delete>",
    0x01000016: "<page_up>",
    0x01000017: "<page_down>",
    0x20: "<space>",
    0x21: "!",
    0x24: "$",
    0x25: "%",
    0x26: "&",
    0x2A: "*",
    0x2B: "+",
    0x2C: ",",
    0x2D: "-",
    0x2E: ".",
    0x2F: "/",
    0x3E: ">",
    0x3C: "<",
    0x3F: "?",
    0x5B: "[",
    0x5C: "\\",
    0x5D: "]",
    0x5F: "_",
    0x60: "`",
    0x7B: "{",
    0x7D: "}",
    0x7E: "~",
    0x0B4: "`",
}


class Earman(
    components.Earman,
    QtCore.QObject,
):
    delisten_key = ["<escape>"]
    key_map: tp.Dict[str, str] = {}
    objectAdded: QtCore.pyqtSignal = QtCore.pyqtSignal(
        object
    )
    keysChanged: QtCore.pyqtSignal = QtCore.pyqtSignal(
        object
    )
    delistenWanted: QtCore.pyqtSignal = QtCore.pyqtSignal()
    matchIsExecuted: QtCore.pyqtSignal = QtCore.pyqtSignal()
    matchIsToBeExecuted: QtCore.pyqtSignal = (
        QtCore.pyqtSignal()
    )

    def setKeyMap(self):
        for name, code in vars(QtCore.Qt.Key).items():
            if name.startswith("Key_"):
                name = name.replace("Key_", "")
                self.key_map[code] = name.lower()
        self.key_map.update(mapping)

    def setup(self) -> None:
        super().setup()
        self.setTimer()
        self.setKeyMap()
        self.setParent(self.app)
        self.connectEarman()

    def connectEarman(self):
        # self.app.buffman.viewAdded.connect(self.add)
        # self.app.plugman.plugAdded.connect(self.add)
        self.app.qapp.installEventFilter(self)

    def setTimer(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.execute)
        self.timer.setSingleShot(True)

    def setPassive(self, modes=None):
        super().setPassive(modes)
        self.keysChanged.emit("")

    def add(self, obj):
        super().add(obj)
        self.objectAdded.emit(obj)

    def eventFilter(self, widget, event):
        if event.type() == QtCore.QEvent.Type.KeyPress:
            self.timer.stop()
            if event.text() and self.handleEvent(event):
                event.accept()
                return True
        return False

    def updatePressedKey(self, key):
        super().updatePressedKey(key)
        digits = ",".join(self.digits())
        text = f"{digits}{self.m_letters}"
        self.keysChanged.emit(text)

    def clearKeys(self, clear_text=False):
        self.timer.stop()
        super().clearKeys()
        if clear_text:
            self.keysChanged.emit("")

    def togglePlug(self, p):
        self.timer.stop()
        self.timer.timeout.disconnect()
        self.timer.timeout.connect(p.toggle)
        self.timer.start(self.wait_run)

    def runAfter(self):
        self.clearKeys()
        self.matchIsExecuted.emit()

    def runBefore(self, func):
        self.matchIsToBeExecuted.emit()

    def setMode(self, mode: str) -> str:
        super().setMode(mode)
        self.modeChanged.emit(self)
        return self.m_mode

    def setSubmode(
        self, submode: str = None, **kwargs
    ) -> str:
        super().setSubmode(submode, **kwargs)
        self.submodeChanged.emit(submode)
        return self.m_submode

    def checkPartial(self, event):
        if super().checkPartial(event):
            return True

    def checkFunctor(self, event):
        if super().checkFunctor(event):
            return True

    def checkPassive(self, event):
        if super().checkPassive(event):
            self.delistenWanted.emit()
            return True

    def checkMatch(self, event):
        if super().checkMatch(event):
            return True

    @classmethod
    def encodeInput(cls, event):
        data = {
            "mod": [],
            "key": event.key(),
            "text": event.text(),
            "type": event.type(),
            "count": event.count(),
            "autorep": event.isAutoRepeat(),
        }
        mod = event.modifiers()
        if mod & QtCore.Qt.KeyboardModifier.AltModifier:
            data["mod"] += ["AltModifier"]
        if mod & QtCore.Qt.KeyboardModifier.ControlModifier:
            data["mod"] += ["ControlModifier"]
        if mod & QtCore.Qt.KeyboardModifier.ShiftModifier:
            data["mod"] += ["ShiftModifier"]
        return data

    @classmethod
    def decodeInput(
        cls,
        mod={},
        key=None,
        text=None,
        type=None,
        autorep=False,
        count=1,
        **kwargs,
    ):
        if not mod:
            m = (
                QtCore.Qt.KeyboardModifier.KeyboardModifier.NoModifier
            )
        else:
            m = getattr(QtCore.Qt, mod[0])
            for i in mod[1:]:
                m = m or getattr(QtCore.Qt, i)
        return QtGui.QKeyEvent(
            type,
            key,
            m,
            text=text,
            autorep=autorep,
            count=count,
        )

    def parseEvent(self, event):
        cmd = "{text}"
        shift = QtCore.Qt.KeyboardModifier.ShiftModifier
        ctrl = QtCore.Qt.KeyboardModifier.ControlModifier
        if event.modifiers() & ctrl:
            cmd = "<c-{text}>"
        text = self.key_map.get(event.key(), "")
        if event.modifiers() & shift:
            text = text.upper()
        return cmd.format(text=text)
