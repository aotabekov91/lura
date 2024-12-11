from plug import Plug, tag

from .view import HelpView

class Help(Plug):

    def setup(self):
        super().setup()
        self.m_data={}
        if self.app.running:
            self.gatherHelpFiles()
        else:
            self.app.appSoonStarts.connect(
                    self.gatherHelpFiles)

    def gatherHelpFiles(self):
        plugs=self.app.plugman.plugs
        for name, plug in plugs.items(): 
            name=name.lower()
            file=plug.getFile('help.md')
            if file:
                data={'file': file}
                self.m_data[name]=data

    def readHelp(self, file):
        with open(file, 'r') as f:
            return f.read()

    @tag('(exec)')
    def help(self, command, **kwargs):
        data=self.m_data.get(command, None)
        if data:
            text=data.get('text', None)
            if text is None:
                file=data.get('file', None)
                data['text']=self.readHelp(file)
                tile=self.app.view.main.current
                if tile:
                    view=HelpView(app=self.app)
                    view.setMarkdown(data['text'])
                    tile.addView(view=view)
                    view.activate()
