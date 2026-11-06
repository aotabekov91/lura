from PyQt6 import QtCore

from plug import Plug, tag, deleg

class Do(Plug, QtCore.QObject):

    @tag('<c-d>(normal)')
    def activate(self, view=None, **kwargs):
        view=view or self.app.stateman.view()
        agent=self.app.delegman.getAgent(
                mode='do', action='do', view=view)
        if agent and view:
            self.app.stateman.activate(mode='do')

    @tag('<c-[>/<escape>/<c-d>(do[any])')
    def octivate(self, view=None, **kwargs):
        self.app.stateman.activate(mode='normal')

    @tag('j(do)')
    def redo(self, view=None, xrange=[1], **kwargs):
        view=view or self.app.stateman.subview()
        kwargs.update({'kind': 'redo', 'xrange': xrange})
        self.app.delegman.delegate(
                action='do', mode='do', view=view, data=kwargs)

    @tag('k(do)')
    def undo(self, view=None, xrange=[1], **kwargs):
        view=view or self.app.stateman.subview()
        kwargs.update({'kind': 'undo', 'xrange': xrange})
        self.app.delegman.delegate(
                action='do', mode='do', view=view, data=kwargs)
