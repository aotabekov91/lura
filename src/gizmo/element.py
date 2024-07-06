class Element:
    def __init__(
        self,
        id=None,
        data=None,
        index=None,
        model=None,
        identifier=None,
        **kwargs,
    ):
        self.m_id = id
        self.m_data = data
        self.m_index = index
        self.m_model = model
        self.m_kwargs = kwargs
        self.m_identifier = identifier
        super().__init__()
        if data:
            self.setData(data)
        self.setup()

    def id(self):
        return self.m_id

    def setId(self, idx):
        self.m_id = idx

    def identifier(self):
        return self.m_identifier

    def setIdentifier(self, idx):
        self.m_identifier = idx

    def setup(self):
        self.updateKlass()

    def updateKlass(self):
        pass

    def data(self, idx=None):
        if not idx:
            return self.m_data
        return self.m_data.get(idx, None)

    def setData(self, data):
        self.m_data = data
        # self.dataReset.emit()

    def updateData(self, data):
        self.m_data.update(data)
        # self.dataUpdated.emit()

    def model(self):
        return self.m_model

    def setModel(self, model):
        self.m_model = model

    def index(self):
        return self.m_index

    def setIndex(self, idx):
        self.m_index = idx
