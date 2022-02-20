from PyQt5.QtCore import *
from lura.render.base import Annotation

class WebAnnotation(Annotation):

    def setPage(self, document):
        self.m_page=document

    def page(self):
        return self.m_page

    def getAnnotationData(self):
        data={'quote':QJsonValue(self.quote()),
                'text': QJsonValue(self.content()),
                'id': QJsonValue(self.id()),
                'ranges': self.getRanges()}
                
        return data

    def getRanges(self):
        ranges=[]
        for m_range in self.position().split('_'):
            m_range=m_range.split(':')
            r={'start':m_range[0],
                    'startOffset': m_range[1],
                    'end': m_range[2],
                    'endOffset': m_range[3]}
            ranges+=[QJsonValue(r)]
        return ranges
               
    def setAnnotationData(self, data):
        self.a_quote=data['quote'].toString()
        self.a_content=data['text'].toString()
        self.a_tag=data['tags'].toString()
        self.a_ranges=data['ranges'].toArray()

    def setId(self, aid):
        self.m_id=aid
        if hasattr(self, 'a_quote'): 
            self.setQuote(self.a_quote)
            self.setContent(self.a_content)
            self.setPosition(self.getPosition())

    def getQuote(self):
        return self.a_quote

    def getPosition(self):
        ranges=[]
        for r in self.a_ranges:
            r=r.toObject()
            start=r['start'].toString()
            startOffset=r['startOffset'].toString()
            end=r['end'].toString()
            endOffset=r['end'].toString()
            ranges+=[f'{start}:{startOffset}:{end}:{endOffset}']
        return '_'.join(ranges)

