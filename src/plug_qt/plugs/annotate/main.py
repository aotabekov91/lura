from PyQt6 import QtCore, QtGui

from plug import Plug, tag, deleg

from .model import AnnotateModel

class Annotate(Plug, QtCore.QObject):

    default_color='green'
    modelCreated=QtCore.pyqtSignal(object)

    def setup(self):
        super().setup()
        self.m_models={}
        self.app.buffman.viewCreated.connect(
                self.createModel)
        self.setMapping()

    def setDefaultColor(self):
        rgb=QtGui.QColor(self.default_color)
        self.m_default_color=[rgb.redF(), rgb.greenF(), rgb.blueF()]

    def mapping(self):
        return self.m_functions

    def setMapping(self):
        self.m_functions={}
        self.setDefaultColor()
        settings=self.m_config.get('Mapping', {})
        for kind, mapping in settings.items():
            self.m_functions[kind.lower()]={}
            for function, data in mapping.items():
                key=data.get('key', None) 
                color=data.get('color', None)
                if color:
                    rgb=QtGui.QColor(color)
                    red=rgb.redF()
                    green=rgb.greenF()
                    blue=rgb.blueF()
                    color=[red, green, blue]
                else:
                    color=self.m_default_color
                data['color']=color
                data['function']=function
                self.m_functions[kind.lower()][key]=data

    @deleg('getModel@(annotate)')
    def getModel(self, model=None, **kwargs):
        return self.m_models.get(model, None)

    def createModel(self, view):
        model=view.model()
        agent=self.app.delegman.getAgent(
                mode='annotate', model=model, delegate='model')
        if agent:
            model=view.model()
            amodel=AnnotateModel(
                    app=self.app, source=model)
            self.modelCreated.emit(amodel)
            self.m_models[model]=amodel
            return amodel

    @deleg('addAnnotation@(annotate)')
    def addAnnotation(self, view=None, selection=None, **kwargs):
        amodel=self.getModel(view.model())
        if selection and amodel:
            data=selection.data()
            return amodel.add(model=view.model(), data=data, **kwargs)

    @deleg('updateAnnotation@(annotate)')
    def updateAnnotation(self, view=None, selection=None, **kwargs):
        amodel=self.getModel(view.model())
        if selection and amodel:
            return amodel.update(
                    model=view.model(), anntation=selection, **kwargs)

    @deleg('removeAnnotation@(annotate)')
    @tag('d(annotate)')
    def removeAnnotation(
            self, view=None, selection=None, **kwargs):
        if not view:
            view=self.app.stateman.view()
        if not selection:
            selection=self.app.delegman.delegate(
                    action='getSelection',
                    data={'view': view})
        amodel=self.getModel(view.model())
        if amodel and selection:
            return amodel.remove(
                    model=view.model(), annotation=selection, **kwargs)
                
    @deleg('getAnnotation@(annotate)')
    def getAnnotation(self, view=None, **kwargs):
        amodel=self.getModel(view.model())
        if amodel:
            return amodel.get(view=view, model=view.model(), **kwargs)

    @tag("<c-h>(annotate)")
    def addHighlightAnnotation(self, xrange=[1], **kwargs):
        kwargs['annotation_kind']='highlight'
        self.setAnnotation(xrange=xrange, **kwargs)

    @tag("<c-c>(annotate)")
    def addCaretAnnotation(self, xrange=[1], **kwargs):
        kwargs['annotation_kind']='caret'
        self.setAnnotation(xrange=xrange, **kwargs)

    @tag("<c-s>(annotate)")
    def addStrikeoutAnnotation(self, xrange=[1], **kwargs):
        kwargs['annotation_kind']='strikeout'
        self.setAnnotation(xrange=xrange, **kwargs)

    @tag("<c-t>(annotate)")
    def addTextAnnotation(self, xrange=[1], **kwargs):
        kwargs['annotation_kind']='text'
        self.setAnnotation(xrange=xrange, **kwargs)

    @tag("<c-u>(annotate)")
    def addUnderlineAnnotation(self, xrange=[1], **kwargs):
        kwargs['annotation_kind']='underline'
        self.setAnnotation(xrange=xrange, **kwargs)

    @deleg('annotate@(any)')
    @tag('<c-a>(normal/visual)')
    def activate(self, view=None, submode=None, **kwargs):
        super().activate()
        if not view:
            view=self.app.stateman.view()
        self.app.stateman.activate(
                moder=self,
                mode='annotate',
                submode=submode,
                **kwargs)
        data=kwargs.copy()
        data['view']=view
        self.app.delegman.delegate(
                mode='annotate', 
                submode=submode, 
                action='activate',
                data=data)

    @deleg('normal@(annotate)')
    @tag('<c-a>/<escape>(annotate)')
    def octivate(self, view=None, submode=None, **kwargs):
        super().octivate()
        if not view:
            view=self.app.stateman.view()
        if not submode:
            submode=self.app.stateman.submode()
        data=kwargs.copy()
        data['view']=view
        self.app.delegman.delegate(
                mode='annotate', 
                submode=submode, 
                action='octivate',
                data=data)
        self.app.stateman.activate()

    def getAnnotationColor(self, xrange=[1], kind=None):
        if xrange:
            key=xrange[-1]
            mapping=self.m_functions.get(kind, {})
            data=mapping.get(key, {})
            return data.get('color', self.m_default_color)
        return self.m_default_color

    def setAnnotation(
            self, 
            view=None, 
            selection=None, 
            xrange=[1], 
            annotation_kind=None,
            **kwargs
            ):
        annotation=None
        if view is None:
            view=self.app.stateman.view()
        if not selection:
            selection=self.app.delegman.delegate(
                    action='getSelection', data={'view': view})
        if selection:
            color=self.getAnnotationColor(xrange, annotation_kind)
            selection['annotation_color']=color
            selection['annotation_kind']=annotation_kind
            annotation=self.addAnnotation(
                    view=view, selection=selection)
            self.app.delegman.delegate(
                    action='clearSelection', data={'view': view})
            self.app.stateman.activate()
        else:
            self.app.delegman.delegate(
                    mode='normal',
                    action='hint',
                    data={'view': view, 'submode': 'word'})
        return annotation
