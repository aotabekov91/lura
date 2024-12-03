from gizmo.utils import tag
from gizmo.ui.qt.utils.view import TabView

class Tab(TabView):

    @tag('T(normal)')
    def toggle(self):
        super().toggle()

    def setup(self):

        super().setup()
        self.setObjectName(self.name)
        self.want=self.m_config.get('want')
        self.wmap=self.m_config.get(
                'widget_map', {})
        self.locator=self.m_config.get(
                'locator', 'position')
        self.include=self.m_config.get(
                'include', {})
        self.exclude=self.m_config.get(
                'exclude', {})
        self.view_kind=self.m_config.get(
                'view_kind', 'ListWidgetView')
        self.view_name=self.m_config.get(
                'view_name', None)
        self.model_name=self.m_config.get(
                'model_name')
        if self.want=='attach':
            self.app.stateman.viewChanged.connect(
                    self.attachView)
        elif self.want=='set':
            self.app.buffman.modelLoaded.connect(
                    self.setupView)

    def setupView(self, m):

        raise
        if m.name!=self.model_name: return
        oname=f'{self.name}View'
        vk=f'views.{self.view_kind}'
        v=self.app.buffman.getView(
                model=m, 
                name=oname,
                view_kind=vk,
                objectName=oname,
                include=self.include,
                exclude=self.exclude,
                widget_map=self.wmap.copy())
        if v:
            s=TabView(
                    app=self.app,
                    suffix_separator='.')
            self.addView(s)
            self.setView(s)
            s.addView(v)
            s.setView(v)

    def attachView(self, view):

        model=view.model()
        if not model: return model
        sub_model=model.submodel(self.model_name)
        if not sub_model: return
        sub_view=self.app.buffman.getView(sub_model)
        if sub_model and not sub_view:
            idx=self.identifier()
            name=f'{self.name}Shell'
            oname=f'{self.name}View'
            tab_view=TabView(
                    app=self.app,
                    suffix_separator='.',
                    )
            self.addView(tab_view)
            self.app.buffman.locate(
                    tab_view, 
                    pos={'TabView': f'!{idx}'},
                    )
            view_kind=f'views.{self.view_kind}'
            pos={self.view_kind:f'!{name}'}
            sub_view=self.app.buffman.getView(
                    sub_model, 
                    # name=oname, # todo 
                    position=pos,
                    view_kind=view_kind,
                    objectName=oname,
                    widget_map=self.wmap,
                    locator=self.locator,
                    include=self.include,
                    exclude=self.exclude,
                    )
            if sub_view:
                tab_view.addView(sub_view)
                tab_view.setView(sub_view)
        if sub_model and sub_view:
            tab_view=sub_view.manager()
            if not tab_view: return
            model=tab_view.manager()
            model.setView(tab_view)
