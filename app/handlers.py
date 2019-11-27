from flask import jsonify, g, request, abort, send_from_directory
from event_calendar.config import config
from werkzeug.utils import secure_filename
import os
from uuid import uuid4 as uuid

def search_for(cls):
    def search():
        args = g.search_args or request.args
        q    = cls.search( **args )

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
