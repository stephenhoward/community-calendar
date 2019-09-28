
from flask.json import JSONEncoder
from connexion.resolver import RestyResolver
from event_calendar.database import DB
from event_calendar.config   import config
import connexion

class ExtendedJSONEncoder(JSONEncoder):

    def default(self,obj):
        if hasattr(obj,'dump') and callable( getattr(obj,'dump') ):
            return obj.dump()
        else:
            return JSONEncoder.default(self,obj)


def create_app():

    db    = DB()
    flask = connexion.FlaskApp(__name__, specification_dir='../config/')

    flask.app.json_encoder = ExtendedJSONEncoder
    flask.app.config['MAX_CONTENT_LENGTH'] = config.get('uploads','max_upload_size')
    with open('/var/calendar/secrets/jwt_private.pem', 'rb') as fh:
        flask.app.config['JWT_PRIVATE_KEY'] = fh.read()
    with open('/var/calendar/secrets/jwt_public.pem', 'rb') as fh:
        flask.app.config['JWT_PUBLIC_KEY'] = fh.read()

    flask.add_api('openapi.yaml',resolver=RestyResolver('app'))

    @flask.app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return flask.app

