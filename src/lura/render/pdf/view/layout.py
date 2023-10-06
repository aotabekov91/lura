from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class SinglePage:

    def __init__(self, settings):

        self.s_settings=settings
        self.viewportPadding=settings.get('viewportPadding', 0) 

    def visibleWidth(self, viewportWidth):

        pageSpacing=self.s_settings.get('pageSpacing', 0.0)
        return viewportWidth-self.viewportPadding#-2.*pageSpacing

    def prepareLayout(self, 
                      pageItems, 
                      rightToLeftMode, 
                      left, 
                      right, 
                      height):

        pageSpacing=self.s_settings.get('pageSpacing', 0.0)
        pageHeight=0.
        for page in pageItems:
            boundingRect=page.boundingRect()
            left=-boundingRect.left()-0.5*boundingRect.width()
            top=height-boundingRect.top()
            page.setPos(left, top)
            pageHeight=boundingRect.height()
            left=min(left, -0.5*boundingRect.width())#-pageSpacing)
            right=max(right, 0.5*boundingRect.width())#+pageSpacing)
            height+=pageSpacing+pageHeight
        return left, right, height

    def leftIndex(self, index): return index

    def rightIndex(self, index, count): return index

    def nextPage(self, page, count): return min(page+1, count)

    def previousPage(self, page, count): return max(page-1, 1)

    def currentPage(self, page): return page


class Layout:

    def __init__(self, documentView):

        self.s_settings=documentView.s_settings
        self.fromLayoutMode(
                self.s_settings.get(
                    'layoutMode', 'SinglePage'))

    def layoutMode(self): return self.m_layoutMode

    def leftIndex(self, index): 
        return self.m_layoutMode.leftIndex(index)

    def rightIndex(self, index, count): 
        return self.m_layoutMode.rightIndex(index, count)

    def fromLayoutMode(self, layoutMode):

        layoutModes={'SinglePage': SinglePage}
        self.m_layoutMode=layoutModes[layoutMode](
                self.s_settings)

    def visibleWidth(self, viewportWidth): 
        return self.m_layoutMode.visibleWidth(viewportWidth)

    def visibleHeight(self, viewportHeight):

        pageSpacing=self.s_settings.get('pageSpacing', 0.0)
        return viewportHeight-2.0*pageSpacing

    def prepareLayout(self, 
                      pageItems, 
                      rightToLeftMode=False, 
                      left=0., 
                      right=0, 
                      height=0.):

        return self.m_layoutMode.prepareLayout(
                pageItems, rightToLeftMode, left, right, height)

    def nextPage(self, page, count): 
        return self.m_layoutMode.nextPage(page, count)

    def previousPage(self, page, count): 
        return self.m_layoutMode.previousPage(page, count)

    def currentPage(self, page): 
        return self.m_layoutMode.currentPage(page)
