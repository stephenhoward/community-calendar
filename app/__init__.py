
from flask.json import JSONEncoder

class ExtendedJSONEncoder(JSONEncoder):

    def default(self,obj):
        if hasattr(obj,'dump') and callable( getattr(obj,'dump') ):
            return obj.dump()
        else:
            return JSONEncoder.default(self,obj)


def create_app():
    import connexion
    from connexion.resolver import RestyResolver
    from event_calendar.database import DB
    from event_calendar.config   import config

    db    = DB()
    flask = connexion.FlaskApp(__name__, specification_dir='../config/')

    flask.app.json_encoder = ExtendedJSONEncoder
    flask.app.config['MAX_CONTENT_LENGTH'] = config.get('uploads','max_upload_size')
    flask.add_api('openapi.yaml',resolver=RestyResolver('app'))

    @flask.app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return flask.app

