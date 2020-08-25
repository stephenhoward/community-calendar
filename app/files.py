from flask import jsonify, g, request, abort, send_from_directory
from event_calendar.config import config
from event_calendar.query_builder import from_query_string
from event_calendar.model.comment import BaseComment
from werkzeug.utils import secure_filename
import os
from uuid import uuid4 as uuid

def _file_extension(filename):
    if '.' not in filename:
        return None

    return filename.rsplit('.',1)[1].lower()

def upload_file_for(cls):
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

        return cls( filename = filename )
        return jsonify( uploaded_file )

def serve_file_for(cls):
    def serve_file(**kwargs):
        file = cls.get(kwargs[id])
        return send_from_directory(cls.path(),file.filename)
    return serve_file
