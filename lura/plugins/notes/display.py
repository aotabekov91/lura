from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .note import Note

from lura.core.widgets import Menu

from lura.core.widgets.tree.menus import MapMenu
from lura.core.widgets.tree.menus import ChangeMenu
from lura.core.widgets.tree.menus import ToggleMenu

from lura.core.widgets.tree import Item
from lura.core.widgets.tree import TreeView

from lura.render.map import BaseMapDocument

class Display(QWidget):

    def __init__(self, parent, settings):
        super().__init__(parent.window)
        self.m_parent=parent
        self.window=parent.window
        self.s_settings=settings
        self.location='left'
        self.name='Notes'
        self.setup()

    def resizeEvent(self, event):
        self.m_view.setFixedWidth()

    def setup(self):

        self.activated=False

        self.m_view=TreeView(self)
        self.m_model=BaseMapDocument()
        self.m_view.setModel(self.m_model)

        mapping={getattr(self, f):v for f, v in self.s_settings['Menu'].items()}
        self.m_noteMenu=Menu(self, mapping)
        self.m_changeMenu=ChangeMenu(self)
        self.m_toggleMenu=ToggleMenu(self)
        self.m_mapMenu=MapMenu(self)

        layout=QVBoxLayout(self)
        layout.addWidget(self.m_view)
        layout.addWidget(self.m_noteMenu)
        layout.addWidget(self.m_changeMenu)
        layout.addWidget(self.m_toggleMenu)
        layout.addWidget(self.m_mapMenu)

        self.fuzzy = self.window.plugin.fuzzy
        self.fuzzy.fuzzySelected.connect(self.actOnFuzzy)

        self.window.setTabLocation(self, self.location, self.name)
        self.setActions()

    def hideMenus(self):
        self.m_noteMenu.hide()
        self.m_mapMenu.hide()
        self.m_changeMenu.hide()
        self.m_toggleMenu.hide()
        self.m_view.setFocus()

    def setActions(self):
        self.actions=[]
        for func, key in self.s_settings['shortcuts'].items():

            m_action=QAction(f'({key}) {func}')
            m_action.setShortcut(QKeySequence(key))
            m_action.setShortcutContext(Qt.WidgetWithChildrenShortcut)
            self.actions+=[m_action]
            m_action.triggered.connect(getattr(self, func))
            self.addAction(m_action)

    def toggleNoteMenu(self):
        self.hideMenus()
        self.m_noteMenu.toggle()

    def toggleMapMenu(self):
        self.hideMenus()
        self.m_mapMenu.toggle()

    def toggleToggleMenu(self):
        self.hideMenus()
        self.m_toggleMenu.toggle()

    def toggleChangeMenu(self):
        self.hideMenus()
        self.m_changeMenu.toggle()

    def actOnFuzzy(self, selected, client):
        if self!=client: return
        self.fuzzy.deactivate(self)
        self.setFocus()
        if self.kind in ['open', 'add']:
            self.openOrAdd(selected, client, self.kind)
        elif self.kind=='delete':
            self.delete(selected, client)

    def setFuzzyData(self):

        notes=self.m_parent.db.getAll()
        names=[n['title'] for n in notes]
        nids=[n['id'] for n in notes]

        self.fuzzy.setData(self, nids, names)

    def current(self):
        
        self.hideMenus()
        if self.window.view() is None: return

        self.m_model.clear()
        did=self.window.document().id()
        tag=f'did:{did}'
        tagged=self.window.plugin.tags.getTagged(tag)
        notes=[self.m_parent.get(t['uid']) for t in tagged if t['kind']=='notes']

        for note in notes:
            if note is None: continue
            self.m_model.appendRow(Item(note))

    def toggle(self):

        if not self.activated:

            self.window.activateTabWidget(self)
            self.m_view.setFocus()
            self.toggleNoteMenu()
            self.activated=True

        else:

            self.window.deactivateTabWidget(self)
            self.activated=False

    def add(self):
        self.openOrAdd(kind='add')

    def open(self):
        self.openOrAdd(kind='open')

    def openOrAdd(self, selected=False, client=False, kind=False):

        self.hideMenus()

        if selected is False:

            self.setFuzzyData()
            self.fuzzy.activate(self)
            self.kind=kind

        else:

            if kind=='open': self.m_model.clear()
            note=self.m_parent.db.get(selected)
            self.m_model.appendRow(Item(note))

    def delete(self, selected=False, client=False):

        self.hideMenus()

        if selected is False:

            self.setFuzzyData()
            self.fuzzy.activate(self)
            self.kind='delete'

        else:

            if hasattr(self, 'm_note'):
                if selected==self.m_note.id():
                    if self.m_layout.count()>1:
                        self.m_layout.removeItem(self.m_layout.itemAt(0))
            self.m_parent.db.delete(selected)
