from tempfile import NamedTemporaryFile as TmpFile

import pynvim


class NVim:
    def __init__(self):
        self.inputId = 0
        self.nvim = pynvim.attach(
            "child",
            argv=[
                "/bin/env",
                "nvim",
                "--embed",
                "--headless",
            ],
        )

        self.inputDoneFile = TmpFile()

    def setText(self, text):
        self.buffman()[:] = text.split("\n")

    def text(self):
        return "\n".join(self.buffman()[:])

    def buffman(self):
        return self.nvim.current.buffman

    def cursorPosition(self):
        return self.nvim.windows[0].cursor

    def cursorAnchor(self):
        return [
            self.nvim.eval('line("v")'),
            self.nvim.eval('col("v")'),
        ]

    def keyPress(self, key):
        self.inputId += 1
        self.nvim.input(key)
        self.nvim.call(
            "writefile",
            [self.inputId],
            self.inputDoneFile.name,
            async_=True,
        )

    def mode(self):
        return self.eval("mode()")

    def commandLine(self):
        return self.eval("getcmdline()")

    def commandLineType(self):
        return self.eval("getcmdtype()")

    def byte(self, row, col):
        cmd = "line2byte(" + str(row) + ")"
        return self.eval(cmd) + col - 1

    def eval(self, expr):
        return self.nvim.eval(expr)

    def isBlocked(self):
        with open(self.inputDoneFile.name, "r") as f:
            data = f.read().strip()
            return data != str(self.inputId)
        return False
