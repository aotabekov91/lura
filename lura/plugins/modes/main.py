from lura.utils import Plugin

from .visual import Visual
from .normal import Normal
from .command import Command

class Modes(Plugin):

    def __init__(self, app):

        super().__init__(app)

        self.input=Normal(app)
        self.visual=Visual(app)
        self.command=Command(app)
