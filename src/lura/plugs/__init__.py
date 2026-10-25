from lura.plugs.fitz91 import PdfFitz
from lura.plugs.fitz_normal_goto import FitzNormalGoTo
from lura.plugs.fitz_annotate import FitzAnnotate
from lura.plugs.fitz_annotate_edit import FitzAnnotationEdit
from lura.plugs.fitz_copy import FitzCopy
from lura.plugs.fitz_fullscreen import FitzFullscreen
from lura.plugs.fitz_grayscale import FitzGrayscale
from lura.plugs.fitz_hint_annotation import FitzAnnotationHint
from lura.plugs.fitz_hint_link import FitzLinkHint
from lura.plugs.fitz_hint_box import FitzBoxHint
from lura.plugs.fitz_hint_block import FitzBlockHint
from lura.plugs.fitz_outline import FitzOutline
from lura.plugs.fitz_rotate import FitzRotate
from lura.plugs.fitz_search import FitzSearch
from lura.plugs.fitz_selection import FitzSelection
from lura.plugs.fitz_yank_selection import FitzYankSelection
from lura.plugs.fitz_zoom import FitzZoom

# todo
# from lura.plugs.fitz_visual_band import FitzBandVisual 
# from lura.plugs.fitz_visual_box import FitzBoxVisual 
from lura.plugs.fitz_visual_block import FitzBlockVisual 

def get_base_plugs():
    return [
            PdfFitz,
            FitzNormalGoTo,
            FitzCopy,
            FitzAnnotate,
            FitzAnnotationEdit,
            FitzFullscreen,
            FitzGrayscale,
            FitzAnnotationHint,
            FitzLinkHint,
            FitzBoxHint,
            FitzBlockHint,
            FitzOutline,
            FitzRotate,
            FitzSearch,
            FitzSelection,
            FitzBlockVisual,
            FitzYankSelection,
            FitzZoom,
            ]
