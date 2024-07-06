class Item:
    def __init__(
        self,
        config={},
        app=None,
        view=None,
        index=None,
        parent=None,
        element=None,
        identifier=None,
        **kwargs,
    ):
        self.app = app
        self.m_id = index
        self.m_view = view
        self.m_config = config
        self.m_element = element
        self.m_identifier = identifier
        self.m_kwargs = kwargs
        super().__init__(parent=parent)
        self.setup()
        self.setView(view)
        self.setElement(element)

    def identifier(self):
        return self.m_identifier

    def setIdentifier(self, identifier):
        self.m_identifier = identifier

    def view(self):
        return self.m_view

    def setView(self, view):
        self.m_view = view

    def setup(self):
        pass

    def element(self):
        return self.m_element

    def update(self):
        pass

    def setElement(self, element):
        self.m_element = element

    def index(self):
        return self.m_id

    def setIndex(self, idx):
        self.m_id = idx
