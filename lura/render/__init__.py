from .pdf import PdfPage
from .pdf import PdfDocument
from .pdf import PdfAnnotation

# from .web import WebPage
# from .web import WebDocument
# from .web import WebAnnotation

from .map import MapDocument

def loadDocument(filePath):
    if filePath.lower().endswith('pdf'): 
        return PdfDocument(filePath)
    # if filePath.lower().startswith('http'): 
        # return WebDocument(filePath)
    if filePath.lower().startswith('map'):
        if 'new' in filePath: return MapDocument()
        return MapDocument(int(filePath.replace('map:', '')))

def createAnnotation(kind):
    if kind=='pdf': return PdfAnnotation() 
    # if kind=='web': return WebAnnotation()
