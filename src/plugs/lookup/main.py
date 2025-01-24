import json

from PyQt6 import QtGui

from plug import tag, Plug
from plug import Plug, Element, Model, Factory

from .view import LookupView
from .define import get_json

class Lookup(Plug):

    def setup(self):
        super().setup()
        self.m_cache={}
        self.setupView()

    def setupView(self):
        self.view=self.app.buffman.createView(
                LookupView, None)

    @tag('(exec)')
    def lookup(self, text):
        self.lookUp(text=text)

    @tag(['<c-D>(normal)', '<c-D>/<c-[>/<escape>(normal)[LookupView]'])
    def toggle(self):
        self.view.toggle()

    @tag('<c-d>(hint)')
    def lookUp(self, text=None, selection=None, view=None, **kwargs):
        if not text:
            if not view:
                view=self.app.stateman.view()
            if not selection:
                selection=self.app.delegman.delegate(
                        action='getSelection', data={'view': view})
            if selection:
                text=selection['text']
        if text:
            model=self.getFromCache(text)
            if model is None:
                definition=get_json(text)
                if definition:
                    json_data=json.loads(definition)
                    model=self.setDefinition(text, json_data)
                else:
                    model=self.setDefinition(text, {})
            if model:
                self.view.setModel(model)
                self.view.activate()

    def setDefinition(self, word, definition):
        if definition:
            model=self.parseDefinition(definition)
        else:
            model={}
        self.m_cache[word]=model
        return model

    def getFromCache(self, text):
        return self.m_cache.get(text, None)

    def parseDefinition(self, definition):
        eklass = Factory(
                QtGui.QStandardItem, Element)
        mklass = Factory(
                QtGui.QStandardItemModel, Model)
        model = mklass(
            name="WordDefinition", element_class=eklass)
        self.populateModel(model, definition)
        return model

    def populateModel(self, model, definition):
        root = model.invisibleRootItem()
        for data in definition:
            word=data['word']
            item=QtGui.QStandardItem(word)
            root.appendRow(item)
            meanings=data['meanings']
            for meaning in meanings:
                definitions=meaning['definitions']
                parts_of_speach=meaning['partOfSpeech']
                for def_data in definitions:
                    if 'definition' in def_data:
                        meaning=def_data['definition']
                        def_item=QtGui.QStandardItem(meaning)
                        if 'example' in def_data:
                            example=def_data['example']
                            exp_item=QtGui.QStandardItem(example)
                            def_item.appendRow(exp_item)
                        item.appendRow(def_item)
