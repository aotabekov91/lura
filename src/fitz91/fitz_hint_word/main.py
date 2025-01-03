from PyQt6 import QtCore, QtGui

from plug import Plug

class FitzWordHint(Plug):

    def setup(self):
        super().setup()
        self.m_hint=''
        self.m_cache={}
        self.m_hints={}
        if self.app.running:
            self.addAgent()
        else:
            self.app.appSoonStarts.connect(
                    self.addAgent)

    def addAgent(self):
        holder=self.app.plugman.getPlug('Hint')
        if holder:
            holder.addAgent('hintWord', 'FitzView', self)

    def words(self, model):
        return self.m_cache.get(model, None)

    def cacheModel(self, model):
        if not model in self.m_cache:
            self.m_cache[model]={}

    def getWords(self, item):
        element=item.element()
        idx=element.index()
        model=element.model()
        cache=self.m_cache[model]
        alist=cache.get(idx, None)
        if alist is None:
            alist = []
            text_page = element.data().get_textpage()
            for box in text_page.extractWORDS():
                xpos, ypos = box[0], box[1]
                width=box[2]-xpos
                height=box[3]-ypos
                data=(xpos, ypos, width, height)
                alist.append({
                    "text": box[4],
                    "box": [element.unify(data)]})
            cache[idx]=alist
        return alist

    def assignHints(self, view):
        plugs=self.app.plugman.plugs
        hinter=plugs.get('Hint')
        items=view.visibleItems()
        all_words=[]
        for item in items: 
            words=self.getWords(item)
            for word in words:
                word['item']=item
            all_words+=words
        _, hints=hinter.generateHints(all_words)
        self.m_hints=hints
        for hint, word in hints.items():
            word['hint']=hint

    def activate(self, view=None, **kwargs):
        if view:
            model=view.model()
            self.cacheModel(model)
            self.assignHints(view)
            self.app.stateman.setFunctor(functor=self.functor)
            view.itemPainted.connect(self.paint)
            view.redraw()

    def octivate(self, view=None, **kwargs):
        if view:
            self.m_hint=''
            self.app.stateman.setFunctor()
            view.itemPainted.disconnect(self.paint)
            view.redraw()

    def paint(self, painter, ops, widget, item):
        painter.save()
        pen = QtGui.QPen(
                QtCore.Qt.GlobalColor.red, 0.0)
        painter.setPen(pen)
        words=self.getWords(item)
        for word in words:
            hint=word.get("hint")
            box = word.get("box")[0]
            if not self.checkHint(hint):
                continue
            rect =item.mapToItem(box, unified=True)
            painter.drawText(rect.topLeft(), hint)
        painter.restore()

    def checkHint(self, hint):
        return self.m_hint==hint[:len(self.m_hint)]

    def select(self, view, data):
        selector=self.app.plugman.getPlug('Selection')
        if selector:
            selection=selector.create(
                    view=view, data=data)
            selector.select(view, selection=selection) 
        hinter=self.app.plugman.getPlug('Hint')
        hinter.octivate(view=view)
        visual=self.app.plugman.getPlug('Visual')
        if visual:
            agent=visual.getAgent(view=view)
            if agent:
                self.app.stateman.activate(
                        mode='visual', submode='word')

    def functor(self, key, earman):
        self.m_hint=key
        view=self.app.stateman.view()
        if self.m_hint in self.m_hints:
            data=self.m_hints.get(self.m_hint)
            self.select(view, data)
            view.redraw()
            return True
        for hint in self.m_hints:
            if self.checkHint(hint):
                view.redraw()
                return True
        self.m_hint=''
        view.redraw()
        return False
