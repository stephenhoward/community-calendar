
def create_app():
    import connexion

    from connexion.resolver import RestyResolver

    from app.site       import site
    from app.events     import events
    from app.categories import categories
    from event_calendar.database import DB

    db    = DB()
    flask = connexion.FlaskApp(__name__, specification_dir='../config/')

    flask.app.register_blueprint(events)

    flask.add_api('openapi.yaml',resolver=RestyResolver('app'))

    @flask.app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return flask.app

