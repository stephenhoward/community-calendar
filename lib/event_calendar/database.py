from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, session
from sqlalchemy.ext.declarative import declarative_base
from event_calendar.config import config, Singleton

Base = declarative_base()

class DB(object, metaclass=Singleton):

    engine  = None
    session = None

    def __init__(self):
        self.build_engine()

    def create_db(self):
        import event_calendar.model.user
        import event_calendar.model.event
        import event_calendar.model.category
        import event_calendar.model.image
        import event_calendar.model.location

        self._db_exec('create database ' + config.get('db')['database'])
        Base.metadata.create_all(bind=self.engine)

    def destroy_db(self):
        session.close_all_sessions()
        self.engine.dispose()
        self._db_exec('drop database ' + config.get('db')['database'])

    def _db_exec(self,sql):
        db_config = config.get('db')

        conn = create_engine(
            'postgresql://' + db_config['credentials'] + \
            '@' + db_config['host'] + '/postgres'
        ).connect()
        conn.execute("commit")
        conn.execute(sql)
        conn.close()

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
