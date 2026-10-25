from PyQt6 import QtCore

from plug import Plug

class FitzAnnotationEdit(Plug):

    def setup(self):
        super().setup()
        if self.app.running:
            self.addAgent()
        else:
            self.app.appSoonStarts.connect(
                    self.addAgent)

    def addAgent(self):
        editor=self.app.plugman.getPlug('AnnotationEdit')
        if editor:
            editor.addAgent('FitzView', self)

    def mapToUI(self, point, ui, match):
        parent = ui.parent()
        if not parent:
            return point
        elif ui==match:
            return point
        current = ui.mapToParent(point)
        return self.mapToUI(current, parent, match)

    def getGeometry(
            self, 
            view=None, 
            annotation=None, 
            xpos=None, 
            ypos=None, 
            **kwargs,
            ):
        if annotation:
            boxes=annotation['box']
            if boxes and view:
                box=boxes[-1]
                item=annotation['item']
                bottom_right=box.bottomRight()
                bottom_right=item.mapToItem(bottom_right, unified=True)
                bottom_right=item.mapToScene(bottom_right)
                bottom_right=view.mapFromScene(bottom_right)
                if not xpos:
                    xpos=int(bottom_right.x())
                if not ypos:
                    ypos=int(bottom_right.y())
            if xpos and ypos:
                point=QtCore.QPoint(xpos, ypos)
                return self.mapToUI(point, view, self.app.view.main)
