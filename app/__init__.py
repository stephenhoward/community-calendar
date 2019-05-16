
def create_app():
    import connexion

    from connexion.resolver import RestyResolver

    from app.events     import events
    from app.categories import categories

    flask = connexion.FlaskApp(__name__, specification_dir='../config/')

    flask.app.register_blueprint(events)

    flask.add_api('openapi.yaml',resolver=RestyResolver('app'))

    return flask.app

