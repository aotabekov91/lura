from lura.utils import Plugin

from .create import Annotate
from .display import Annotations

class Annotation(Plugin):

    def __init__(self, app):

        super().__init__(app, name='annotation')

        self.annotate=Annotate(self.app)
        self.annotate.setColors(self.colors)

        self.annotations=Annotations(self.app)
        self.annotations.setColors(self.colors)

    def setConfig(self):

        self.config=self.readConfig()
        if self.config.has_section('Colors'):
            self.colors = dict(self.config.items('Colors'))

    def removeById(self, aid):

        self.annotate.removeById(aid)

    def updateData(self):

        self.annotations.updateData()
