class Copy:
    canCopy = True

    def copy(self, *args, **kwargs):
        # s=self.m_state.copy()
        m = self.manager()
        klass = self.__class__
        copy = self.app.buffman.create(
            klass,
            app=self.app,
            config=self.m_config,
        )
        copy.setModel(self.m_model)
        self.app.buffman.saveView(self.m_model, copy)
        copy.setManager(m)
        # copy.setStates(s, want=True)
        return copy
