"""
This module implements a Flask-based JSON API to talk with the annotation store via the
Annotation model.
It defines these routes:
  * Root
  * Index
  * Create
  * Read
  * Update
  * Delete
  * Search
  * Raw ElasticSearch search
See their descriptions in `root`'s definition for more detail.
"""
from __future__ import absolute_import

import json

from flask_cors import cross_origin

from flask import Blueprint, Response
from flask import request
from flask import url_for

from lura.plugins.documents.table import DocumentsTable
from lura.plugins.metadata.table import MetadataTable
from lura.plugins.annotation.table import AnnotationsTable
from lura.plugins.tags.connect import DatabaseConnector as TagDB

store = Blueprint('store', __name__)

CREATE_FILTER_FIELDS = ('updated', 'created', 'consumer', 'id')
UPDATE_FILTER_FIELDS = ('updated', 'created', 'user', 'consumer')


aTable=AnnotationsTable()
dTable=DocumentsTable()
mTable=MetadataTable()
tTabel=TagDB()

def createAnnotation(data):

    data=data.copy()
    document=dTable.getRow({'field':'loc','value':data['url']})
    if len(document)==0:
        document=dTable.writeRow({'loc':data['url']})
        document=dTable.getRow({'field':'loc','value':data['url']})
    document=document[0]
    data['did']=document['id']
    mTable.writeRow({'did':document['id'], 'kind':'website'})

    data['position']=getPosition(data['ranges'])
    data['page']=0
    data.pop('ranges')
    tags=data.pop('tags')
    data.pop('url')
    data['content']=data['text']
    data.pop('text')

    aTable.writeRow(data)
    fields=['did', 'page', 'position', 'quote']
    condition=[{'field':k, 'value':data[k]} for k in fields]
    annotation=aTable.getRow(condition)[0]

    tTabel.setTags(annotation['id'], 'annotations', ';'.join(tags))

    return dict(annotation)

# We define our own jsonify rather than using flask.jsonify because we wish
# to jsonify arbitrary objects (e.g. index returns a list) rather than kwargs.
def jsonify(obj, *args, **kwargs):
    res = json.dumps(obj)
    request=after_request(Response(res, mimetype='application/json', *args, **kwargs))
    return request

@store.after_request
def after_request(response):
    ac = 'Access-Control-'
    rh = response.headers
    # rh[ac + 'Allow-Origin'] = request.headers.get('origin', '*')
    rh[ac + 'Allow-Origin'] = '*'
    rh[ac + 'Expose-Headers'] = 'Content-Length, Content-Type, Location'
    if request.method == 'OPTIONS':
        # rh[ac + 'Allow-Headers'] = ('Content-Length, Content-Type, '
        rh[ac + 'Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        rh[ac + 'Max-Age'] = '86400'
    return response


# ROOT
@store.route('/')
@cross_origin()
def root():
    return jsonify({
        'message': "Annotator Store API",
        'links': {
            'annotation': {
                'create': {
                    'method': 'POST',
                    'url': url_for('.create_annotation', _external=True),
                    'query': {
                        'refresh': {
                            'type': 'bool',
                            'desc': ("Force an index refresh after create "
                                     "(default: true)")
                        }
                    },
                    'desc': "Create a new annotation"
                },
                'read': {
                    'method': 'GET',
                    'url': url_for('.read_annotation',
                                   docid=':id',
                                   _external=True),
                    'desc': "Get an existing annotation"
                },
                'update': {
                    'method': 'PUT',
                    'url':
                    url_for(
                        '.update_annotation',
                        docid=':id',
                        _external=True),
                    'query': {
                        'refresh': {
                            'type': 'bool',
                            'desc': ("Force an index refresh after update "
                                     "(default: true)")
                        }
                    },
                    'desc': "Update an existing annotation"
                },
                'delete': {
                    'method': 'DELETE',
                    'url': url_for('.delete_annotation',
                                   docid=':id',
                                   _external=True),
                    'desc': "Delete an annotation"
                }
            },
            'search': {
                'method': 'GET',
                'url': url_for('.search_annotations', _external=True),
                'desc': 'Basic search API'
            },

        }
    })


# INDEX
@store.route('/annotations')
@cross_origin()
def index():
    return jsonify([dict(a) for a in aTable.getAll()])

# CREATE
@store.route('/annotations', methods=['POST'])
@cross_origin()
def create_annotation():

    if request.json is not None:

        annotation=createAnnotation(request.json)
        request.json.update(annotation)

        location = url_for('.read_annotation', docid=annotation['id'])
        return jsonify(request.json), 201, {'Location': location}


# READ
@store.route('/annotations/<docid>')
@cross_origin()
def read_annotation(docid):
    annotation=dict(aTable.getRow({'field':'id', 'value':docid})[0])
    annotation['text']=annotation['content']
    tags=tTabel.get(docid, 'annotations')
    annotation['tags']=tags.split(';')
    return jsonify(annotation)


# UPDATE
@store.route('/annotations/<docid>', methods=['POST', 'PUT'])
@cross_origin()
def update_annotation(docid):

    if request.json is not None:

        updated = _filter_input(request.json, UPDATE_FILTER_FIELDS)
        updated.pop('id')

        aTable.updateRow({'field': 'id', 'value':docid}, 
                {'content': updated['text'],
                    'quote': updated['quote'],
                    'color': updated['color'],})

        tTabel.setTags(docid, 'annotations', ';'.join(updated['tags']))

        annotation=dict(aTable.getRow({'field':'id', 'value':docid})[0])

        request.json.update(annotation)

        location = url_for('.read_annotation', docid=docid)
        return jsonify(request.json), 201, {'Location': location}


# DELETE
@store.route('/annotations/<docid>', methods=['DELETE'])
@cross_origin()
def delete_annotation(docid):

    annotation=aTable.getRow({'field':'id', 'value':docid})

    if len(annotation)==0:
        return jsonify('Annotation not found. No delete performed.',
                       status=404)
    aTable.removeRow({'field':'id', 'value':dict(annotation[0])['id']})

    return jsonify('', 204)


# SEARCH
@store.route('/search')
@cross_origin()
def search_annotations():
    params = dict(request.args.items())

    if 'filePath' in params:

        url=params['filePath']
        document=dTable.getRow({'field':'loc','value':url})

        if len(document)==0: return jsonify(
                {'total': 0, 'rows':[]})
            
        annotations=aTable.getRow({'field':'did', 'value':document[0]['id']})

        if len(annotations)==0: return jsonify(
                {'total': 0, 'rows':[]})

        jsAnnotations=createAnnotationJS(annotations)

        return jsonify({'total': len(jsAnnotations), 'rows': jsAnnotations})

    return jsonify({'total': 0, 'rows':[]})

def getPosition(ranges):
    m_ranges=[]
    for r in ranges:
        start=r['start']
        startOffset=r['startOffset']
        end=r['end']
        endOffset=r['endOffset']
        m_ranges+=[f'{start}:{startOffset}:{end}:{endOffset}']
    return '_'.join(m_ranges)

def createAnnotationJS(annotations):
    jsAnnotations=[]
    for a in annotations:

        a=dict(a)
        a['text']=a['content']

        a['ranges']=[]
        for m_range in a['position'].split('_'):
            m_range=m_range.split(':')
            a['ranges']+=[{'start':m_range[0],
                    'startOffset': m_range[1],
                    'end': m_range[2],
                    'endOffset': m_range[3]}]

        tags=tTabel.get(a['id'], 'annotations')
        a['tags']=tags.split(';')

        jsAnnotations+=[a]
    return jsAnnotations

def _filter_input(obj, fields):
    for field in fields:
        obj.pop(field, None)
    return obj
