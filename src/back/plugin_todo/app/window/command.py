from ...widget import ListWidget, CommandStack

class CommandWindow(CommandStack):

    def __init__(self, app, *args, **kwargs):

        super(CommandWindow, self).__init__(*args, **kwargs)

        self.app=app
        self.activated=False
        self.setUI()

    def setUI(self):

        self.app.stack.add(self, 'command')
        self.addWidget(ListWidget(exact_match=True, check_fields=['down']), 'mode')

    def activate(self): 

        self.activated=True
        self.app.stack.show(self)
        self.setFixedSize(self.app.stack.size())

    def deactivate(self): 

        self.activated=False
        self.app.stack.show(self.app.main)
