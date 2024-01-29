from gizmo.utils import tag
from threading import Thread, Event

class Slider:

    sliderPauseTime=10
    sliderRestartOnFinish=True

    def setup(self):

        super().setup()
        self.m_sliding=False
        self.m_slider_signal=Event()
        self.app.appSoonQuits.connect(
                self.octivateSlider)

    @tag('s', modes=['normal[any]|^own'])
    def toggleSlider(self, rstart=None):

        if self.m_sliding:
            self.octivateSlider()
        else:
            self.activateSlider(rstart)

    def octivateSlider(self):

        self.m_sliding=False
        self.m_slider_signal.set()
        self.app.ui.moder.setSubmode()

    def activateSlider(self, rstart=None):

        self.m_sliding=True
        self.m_slider_signal.clear()
        rstart=rstart or self.sliderPauseTime
        self.app.ui.moder.setSubmode('slider')

        def start(idx):
            while not self.m_slider_signal.is_set():
                self.item(idx)
                self.m_slider_signal.wait(rstart)
                if self.m_sliding:
                    self.m_slider_signal.clear()
                idx+=1
                c1 = idx>self.count()
                c2 = self.sliderRestartOnFinish
                if c1 and c2: 
                    idx=1
                elif c1: 
                    self.m_sliding=False

        idx=self.m_item.index()
        self.m_slider_thread=Thread(
                target=start, args=(idx,))
        self.m_slider_thread.deamon=True
        self.m_slider_thread.start()
