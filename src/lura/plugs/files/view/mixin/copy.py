class Copy:

    canCopy=True

    def copy(self):

        c=self.__class__(
                app=self.app, 
                name=self.name, 
                index=self.m_id, 
                config=self.m_config)
        idx=self.currentIndex()
        p=self.m_model.filePath(idx)
        x=self.m_model.getPathIndex(p)
        c.setModel(self.m_model)
        c.setRootIndex(x.parent())
        c.setCurrentIndex(x)
        return c
