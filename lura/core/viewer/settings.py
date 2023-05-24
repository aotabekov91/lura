from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from popplerqt5 import Poppler

settings={
        'scaleFactor':1.,
        'scaleMode':{
            'modes':[
                'ScaleFactorMode',
                'FitToPageWidthMode',
                'FitToPageHeightMode'
                ],
            'currentMode': 'FitToPageHeightMode',
            },
        'layout': {
            'modes':[
                'SinglePageLayout',
                'TwoPagesLayout'
                ],
            'currentMode':'SinglePageLayout',
            # 'pageSpacing':2.,
            'pageSpacing':0.,
            'viewportPadding':0,
            },
        'invertColors':False,
        'convertToGrayscale':False,
        'continuousMode':True,
        'pageItem': {
            'decoratePages':False,
            'paperColor':QColor('gray'),
            'drawMode':'DefaultMode',
            'useTiling': False,
            'keepObsoletePixmaps':True,
            'trimMargins':False,
            'tileSize': 1024,
            'annotationOverlay': True,
            'copyToClipboardModifiers':1,
            'decorateLinks':True,
            # 'proxyPadding': 6.,
            'proxyPadding': 0.,
            'annotationOverlay':True,
            }, 
        'documentView':{
                'zoomFactor':1.1,
                },
        'resolution': {
            'resolutionX':72,
            'resolutionY':72,
            'devicePixelRatio':1.
            },
        'rotation':{
            'modes':[
                Poppler.Page.Rotate0,
                Poppler.Page.Rotate90,
                Poppler.Page.Rotate180,
                Poppler.Page.Rotate270,
                ],
            'currentMode':Poppler.Page.Rotate0
            },
        'rubberBandMode': {
            'listener': None,
            },
        'menu': {
                'listener': None
                },

        'drawMode':{
            'modes':[
                'PresentationMode',
                'ThumbnailMode',
                'DefaultMode'],
            'currentMode': 'DefaultMode'
            },
        }
