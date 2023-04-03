import os
import re
import sqlite3
from collections import OrderedDict
from sqlite3 import connect, Row, IntegrityError

from .documents import DocumentsTable
from .annotations import AnnotationsTable

class Tables(OrderedDict):

    def __init__(self, app):
        super().__init__()
        self.app=app
        self.setup()

    def setup(self):
        self.add_table(DocumentsTable, 'documents')
        self.add_table(AnnotationsTable, 'annotations')

    def add_table(self, tableClass, tableName=None): 
        table=tableClass()
        if tableName is None: 
            tableName=table.__class__.__name__.lower().replace('table', '') 
        setattr(self, tableName, table)

    def get(self, tableName, conDict=None, fieldName=None, unique=True):
        table=getattr(self, tableName, None)
        if table is None: return

        if conDict is None: return table.getAll()

        conds=[]
        for key in conDict.keys():
            conds+=[{'field':key, 'value':conDict[key]}]
        results=table.getRow(conds)

        if len(results)==0: return

        if fieldName is None:
            if unique:
                return results[0]
            else:
                return results
        else:
            found=[r[fieldName] for r in results]
            if unique:
                return found[0]
            else:
                return found

    def write(self, tableName, conDict):
        table=getattr(self, tableName, None)
        if table is None: return
        table.writeRow(conDict, update=True)

    def update(self, tableName, conDict, updateDict):
        table=getattr(self, tableName, None)
        if table is None: return
        cond=[]
        for key in conDict.keys():
            cond+=[{'field':key, 'value':conDict[key]}]
        table.updateRow(cond, updateDict)

    def remove(self, tableName, conDict):
        table=getattr(self, tableName, None)
        if table is None: return
        cond=[]
        for key in conDict.keys():
            cond+=[{'field':key, 'value':conDict[key]}]
        table.removeRow(cond)
