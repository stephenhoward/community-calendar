from sqlalchemy import Column, Enum
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.dialects.postgresql import UUID as UUIDColumn
from event_calendar.database import DB
import enum
import yaml
from uuid import UUID, uuid4 as uuid

db    = DB()
codes = yaml.load( open('config/language_codes.yaml','r'), Loader=yaml.FullLoader )

LanguageCode = enum.Enum( 'LanguageCode', codes['LanguageCode']['enum'] )

class Model(object):
    id = Column( UUIDColumn(as_uuid=True), primary_key=True )

    def __init__(self,**kwargs):
        self.update(kwargs)

        if ( not isinstance( self.id, UUID ) ):
            self.id = uuid()

    @classmethod
    def search(cls,**kwargs):
        return cls._search( db.session.query(cls), **kwargs )

    @classmethod
    def _search(cls,query,**kwargs):

        mapper = inspect(cls)

        for key,value in kwargs.items():

            if mapper.attrs[key]:
                query = query.filter_by( **{ key:value } )

        return query

    @classmethod
    def get(cls,id):
        return db.session.query( cls ). \
            filter(cls.id == id). \
            one()

    @classmethod
    def create(cls,dict):
        model = cls(**dict)
        db.session.add(model)
        return model

    def update(self,dict):

        mapper = inspect(type(self))

        for key, value in dict.items():

            attr = mapper.attrs[key]

            if ( isinstance( attr, RelationshipProperty ) ):

                other_cls = attr.mapper.class_

                if ( attr.uselist ):
                    setattr( self, key, list(map(
                        lambda v: v if isinstance(v,other_cls) else other_cls.create(v),
                        value
                    )) )
                else:
                    if ( isinstance( value, other_cls ) ):
                        setattr( self, key, value )
                    else:
                        setattr( self, key, other_cls.create(value) )
            else:
                setattr( self, key, value )

        return self

    def save(self):
        db.session.commit()
        return self

class Translation(Model):
    language = Column( Enum(LanguageCode), primary_key=True )
