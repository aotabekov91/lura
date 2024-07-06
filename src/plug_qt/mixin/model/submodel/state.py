from PyQt6 import QtCore

from plug import Element
from plug_qt.vimo import Model
from plug.utils import Factory


class State:
    hasStates = True

    def setup(self):
        super().setup()
        mklass = Factory(Model, QtCore.QObject)
        eklass = Factory(Element, QtCore.QObject)
        self.m_states = mklass(
            name="state", element_class=eklass
        )
        self.addModel("state", self.m_states)

    def addState(self, data):
        idx = data.get("state")
        e = self.getState(idx)
        if not e:
            self.m_states.createElement(data)
        else:
            self.m_states.updateElement(e, data)

    def getState(self, idx, by="state"):
        return self.m_states.getElement(idx, by=by)

    def delState(self, data):
        idx = data.get("state")
        e = self.getState(idx)
        self.m_states.delElement(e)
