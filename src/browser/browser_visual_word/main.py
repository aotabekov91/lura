from plug import Plug, deleg

class BrowserVisualWord(Plug):

    @deleg('activate@(visual[word])[BrowserView]')
    def activate(self, view=None, **kwargs):
        print('start')
        # todo: if no selection, start hinting

    @deleg('octivate@(visual[word])[BrowserView]')
    def octivate(self, view=None, **kwargs):
        print('finish')

    @deleg('goTo@(visual[word])[BrowserView]')
    def goTo(self, kind='last', view=None, xrange=[1], **kwargs):
        if view:
            script=None
            if kind=='left':
                script=view.scriptize('caret', 'moveToPreviousWord', xrange[-1])
            elif kind=='right':
                script=view.scriptize('caret', 'moveToNextWord', xrange[-1])
            elif kind=='up':
                script=view.scriptize('caret', 'moveUp', xrange[-1])
            elif kind=='down':
                script=view.scriptize('caret', 'moveDown', xrange[-1])
            elif kind=='first':
                script=view.scriptize('caret', 'moveToStartOfLine', xrange[-1])
            elif kind=='last':
                script=view.scriptize('caret', 'moveToEndOfLine', xrange[-1])
            elif kind=='toggle':
                script=view.scriptize('caret', 'toggle')
            if script:
                view.runJSCode(script)
