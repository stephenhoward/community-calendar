from flask import jsonify, g, request, abort, send_from_directory
from event_calendar.config import config
from event_calendar.query_builder import query_from_query_string
from event_calendar.model.comment import BaseComment
from werkzeug.utils import secure_filename
from uuid import uuid4 as uuid

def search(cls,guard):
    def _search():

        guard('search',cls)

        if hasattr(g,'search_args'):
            args = g.search_args
        else:
            args = request.args

        q = query_from_query_string( cls, **args )

        return jsonify( q.all() )
    return _search

def get(cls,guard):
    def _get(id):
        model = _get_model(cls,id, lambda m: guard('get',m))

        return jsonify(model)
    return _get

def post(cls,guard):
    def _post():

        model = cls.create(request.json)

        guard('post',model)

        model.save()
        return jsonify( model )
    return _post

def update(cls,guard):
    def _update(id):

        model = _get_model(cls,id, lambda m: guard('update',m))

        model.update( request.json ).save()
        return jsonify( model )
    return _update

def delete(cls,guard):
    def _delete(id):

        model = _get_model(cls,id, lambda m: guard('delete',m))

        model.delete()
        return jsonify( ok = 1 )
    return _delete

def _get_model(cls,id,guard):
    model = cls.get(id);

    if model:
        guard(model)
        return model
    else:
        abort(404)
