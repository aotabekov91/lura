from gizmo.utils import tag

class GrayScale:

    convertToGrayScale=False

    @tag('c', modes=['normal|^own'])
    def toggleGrayScale(self):

        item=self.currentItem()
        item.toggleGrayScale()
