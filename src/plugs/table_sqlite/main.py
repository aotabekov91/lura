from plug import Plug

from .table import Table

class SQLiteTable(Plug):

    def setup(self):
        super().setup()

    def createTable(self, *args, **kwargs):
        return Table(*args, **kwargs)
