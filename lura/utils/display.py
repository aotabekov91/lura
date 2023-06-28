from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from plugin.app import Display

class LuraDisplay(Display):

    annotationAdded=pyqtSignal(object)
    annotationCreated=pyqtSignal(object)
    annotationRegistered=pyqtSignal(object)
