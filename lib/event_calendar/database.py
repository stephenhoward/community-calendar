from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# TODO: locate database name in a config file, overrideable for testing
engine = create_engine('postgresql://postgres:badpassword@postgres:5432/postgres')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import event_calendar.model.event
    import event_calendar.model.category
    import event_calendar.model.image
    import event_calendar.model.location
    Base.metadata.create_all(bind=engine)