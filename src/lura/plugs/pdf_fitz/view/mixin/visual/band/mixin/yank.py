from PyQt5 import QtCore
from gizmo.plug.utils import tag


class Yank:
    def setup(self):
        super().setup()
        self.m_last_yanked_dir = None

    @tag(["yy", "yt"], modes=["visual[band]|^own"])
    def yankAsText(self, rstart=1, **kwargs):
        if not self.m_band:
            return
        i = self.m_band["item"]
        e = i.element()
        b = self.m_band["box"][0]
        r = e.unity(b)
        r = (r.x(), r.y(), r.x() + r.width(), r.y() + r.height())
        f = e.getBlockText("blocks", clip=r)
        if not f:
            return
        text = []
        for i in range(len(f)):
            t = f[i][4]
            if rstart == 1:
                t = t.replace("\n", " ")
            text += [t]
        text = "\n".join(text)
        if text:
            c = self.app.qapp.clipboard()
            c.setText(text)
        self.app.moder.toggle()
        self.cleanUp()

    @tag("yic", modes=["visual[band]|^own"])
    def yankAsImageToClipboard(self, *args, **kwargs):
        img = self.yankImage()
        if not img:
            return
        self.app.moder.toggle()
        self.cleanUp()

    @tag("yis", modes=["visual[band]|^own"])
    def yankAsImageToSave(self, *args, **kwargs):
        img = self.yankImage()
        if not img:
            return
        self.app.moder.toggle("save", submode="image")
        self.app.ui.bar.activateEdit(
            label="Path",
            edit=self.m_last_yanked_dir,
        )

    @tag(["<c-m>", "<return>"], modes=["save[image]|^own"])
    def saveYankedImage(self, *args, **kwargs):
        img = self.yankImage()
        t = self.app.ui.bar.text()
        try:
            img.save(t)
            fldr = t.rsplit("/", 1)[0]
            self.m_last_yanked_dir = fldr
        except:
            pass
        self.cleanUpYankedImage()

    @tag(["<escape>", "<c-[>"], modes=["save[image]|^own"])
    def cleanUpYankedImage(self, *args, **kwargs):
        self.app.ui.bar.octivateEdit()
        self.app.moder.toggle()
        self.cleanUp()

    def yankImage(self):
        if not self.m_band:
            return
        i = self.m_band["item"]
        b = self.m_band["box"][0]
        mb = i.mapToItem(b, unified=True)
        pxm = i.takePixmap()
        if not pxm:
            return
        crp = pxm.copy(mb.toRect())
        if not crp:
            return
        return crp.toImage()
