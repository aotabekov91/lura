from .pdf import PdfDocument
from .map import MapDocument

def loadDocument(filePath):
    if filePath.lower().endswith('pdf'):
        return PdfDocument(filePath)
    if filePath.lower().startswith('map'):
        if 'new' in filePath:
            return MapDocument()
        return MapDocument(int(filePath.replace('map:', '')))
