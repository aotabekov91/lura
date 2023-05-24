#!/usr/bin/env python
import sys

from lura import Lura

def main():
    app = Lura()
    sys.exit(app.exec_())
