from .base import Event


class KeyEvent(Event):

    def parseKey(self, event):

        key = []
        shift = True
        special = False
        mod = event.modifiers()
        if mod & QtCore.Qt.KeyboardModifier.ControlModifier:
            special = True
            key += ["^C"]
        if mod & QtCore.Qt.KeyboardModifier.ShiftModifier:
            shift = True
        text = event.text()
        if text:
            if shift:
                text = text.upper()
            key += [text]
        if len(key) == 1:
            key = key[0]
            if special:
                key = f"<{key}>"
            return key
        return f'<{"-".join(key)}>'
