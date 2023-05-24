from tables import Tables as TablesForm
from tables import Metadata, Hash, Annotation

class Tables(TablesForm):

    def __init__(self):

        super().__init__()

        self.add_table(Hash, 'hash')
        self.add_table(Metadata, 'metadata')
        self.add_table(Annotation, 'annotation') 
