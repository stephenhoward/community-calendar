from flask import jsonify, request, abort
import app.handlers as handlers
from event_calendar.model.image import Image
from event_calendar.model.org import Org

def post_image():

    if not g.user.has_role('Contributor', for_org = request.form.org_id):
        abort(403)
    
    # image = handlers.upload_file_for(Image)
    image.org_id = request.form.org_id

    image.save()
    return jsonify(image)

def get_image():
    pass

# get_image  = handlers.serve_file_for(Image)
