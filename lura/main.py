#!/bin/bash
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.core.window import WindowManager

import yaml
import argparse

fileLocs=['/home/adam/docs/docs/1raman_kirthi_mastering_python_data_visualization.pdf',
        '/home/adam/docs/docs/1300_math_formulas.pdf']

fileLocs=['https://www.google.com']
configurationFile='/home/adam/code/lura/config.yaml'

def process_cl_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url')
    parser.add_argument('-f', '--file')
    parser.add_argument('open', nargs='?')
    parsed_args, unparsed_args = parser.parse_known_args()
    return parsed_args, unparsed_args

class App:

    def __init__(self, documentLocs=[]):
        super().__init__()
        configuration=self.getConfiguration()
        self.window=WindowManager(configuration)

    def getConfiguration(self): 
        with open(configurationFile, 'r') as stream:
            config = yaml.safe_load(stream)
        return config

if __name__ == "__main__":
    parsed_args, unparsed_args = process_cl_args()
    qt_args = sys.argv[:1] + unparsed_args
    app = QApplication(qt_args)
    mainWin = App()
    if parsed_args.open: mainWin.window.open(parsed_args.open)

    try:
        sys.exit(app.exec_())
    except:
        view=mainWin.window.view()
        if view is not None: view.save()
        raise



