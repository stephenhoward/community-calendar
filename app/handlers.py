from flask import jsonify, g, request, abort, send_from_directory
from event_calendar.config import config
from event_calendar.query_builder import from_query_string
from werkzeug.utils import secure_filename
import os
from uuid import uuid4 as uuid

def search_for(cls):
    def search():
        if hasattr(g,'search_args'):
            args = g.search_args
        else:
            args = request.args

        q = cls.search( *from_query_string( cls, **args ) )

        return jsonify( q.all() )
    return search

def get_for(cls):
    def get(**kwargs):
        model = cls.get(kwargs['id'])

        if ( model ):
            return jsonify( model )
        else:
            abort(404)
    return get

def post_for(cls):
    def post():
        model = cls.create(request.json).save()

        return jsonify( model )
    return post

def update_for(cls):
    def update(id):
        model = cls.get(id)

        if ( model ):
            model.update( request.json ).save()
            return jsonify( model )
        else:
            abort(404)
    return update

def delete_for(cls):
    def delete(id):
        model = cls.get(id);

        if ( model ):
            model.delete()
            return jsonify( ok = 1 )
        else:
            abort(404)
    return delete

def _file_extension(filename):
    if '.' not in filename:
        return None

    return filename.rsplit('.',1)[1].lower()

def upload_file_for(cls):
    def upload_file(**kwargs):
        if 'file' not in request.files:
            abort(400)

        file = request.files['file']
        if file.filename == '':
            abort(400)

        if file:
            file_extension = _file_extension(file.filename)

            if file_extension == None or file_extension not in config.get('uploads','extensions'):
                abort(400)

            filename = str(uuid()) + '.' + file_extension
            file.save( os.path.join( cls.path(), filename ) )

            uploaded_file = cls( filename = filename )
            return jsonify( uploaded_file )
    return upload_file

def serve_file_for(cls):
    def serve_file(**kwargs):
        file = cls.get(kwargs[id])
        return send_from_directory(cls.path(),file.filename)
    return serve_file


def get_comments_for(cls):
    def get_comments(**kwargs):
        model = cls.get(kwargs['id'])
        return jsonify( model.comments )
    return get_comments


def post_comment_for(cls):
    def post(**kwargs):
        model   = cls.get(kwargs['id'])
        comment = model.add_comment(request.json)
        model.save()

        return jsonify( comment )
    return post

def update_comment_for(cls):
    def update(**kwargs):
        model   = cls.get(kwargs['id'])
        comment = model.get_comment(kwargs['comment_id'])

        if ( comment ):
            comment.update( request.json ).save()
            return jsonify( comment )
        else:
            abort(404)
    return update
