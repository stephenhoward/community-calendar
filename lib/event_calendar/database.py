from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from event_calendar.config import config, Singleton

Base = declarative_base()

class DB(object, metaclass=Singleton):

    engine  = None
    session = None

    def __init__(self):
        self.build_engine()

    def create_db(self):
        # import all modules here that might define models so that
        # they will be registered properly on the metadata.  Otherwise
        # you will have to import them first before calling init_db()
        import event_calendar.model.event
        import event_calendar.model.category
        import event_calendar.model.image
        import event_calendar.model.location
        Base.metadata.create_all(bind=self.engine)

    def destroy_db(self):
        # import all modules here that might define models so that
        # they will be registered properly on the metadata.  Otherwise
        # you will have to import them first before calling init_db()
        import event_calendar.model.event
        import event_calendar.model.category
        import event_calendar.model.image
        import event_calendar.model.location
        Base.metadata.create_all(bind=self.engine)

    def build_engine(self):
        db_config = config.get('db')

        self.engine  = create_engine(
            'postgresql://' + db_config['credentials'] + \
            '@' + db_config['host'] + \
            '/' + db_config['database']
        )

        self.session = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
        )
        Base.query = self.session.query_property()
