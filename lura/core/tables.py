from tables import HashTable
from tables import Tables as TablesForm

class Tables(TablesForm):

    def __init__(self, app):
        super().__init__()
        self.app=app
        self.add_table(HashTable, 'hash')
