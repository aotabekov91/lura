from plug import Plug, tag

class Help(Plug):

    @tag('(exec)')
    def help(self, command, **kwargs):
        print(command)
