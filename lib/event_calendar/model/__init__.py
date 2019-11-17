from sqlalchemy import Column, Enum
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.dialects.postgresql import UUID as UUIDColumn
from event_calendar.database import DB
from sqlalchemy.orm.exc import NoResultFound
import enum
import yaml
from uuid import UUID, uuid4 as uuid

db    = DB()
codes = yaml.load( open('config/languages.yaml','r'), Loader=yaml.FullLoader )

LanguageCode  = enum.Enum( 'LanguageCode', list(codes.keys()) )
ContentStatus = enum.Enum( 'ContentStatus', [
    'Draft',
    'Active'
])

class Model(object):
    id = Column( UUIDColumn(as_uuid=True), primary_key=True )

    def __init__(self,**kwargs):
        self.update(kwargs)

        if ( not isinstance( self.id, UUID ) ):
            self.id = uuid()

    @classmethod
    def search(cls,*operators):
        return cls.query.filter(*operators)

    @classmethod
    def get(cls,id):
        try:
            return cls.query.get(id)
        except NoResultFound:
            return None

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
                self.update_attr( key, value )

        return self

    def update_attr(self,attr,value):
        setattr( self, attr, value )

    def save(self):
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def _dont_dump(self):
        return [];

    def dump(self):
        dumped  = {}
        no_dump = self._dont_dump()

        for c in self.__table__.columns:
            if c.name not in no_dump:
                dumped[c.name] = getattr(self,c.name)

        return dumped

class TranslatableModel(Model):

    def dump(self):
        d = super().dump()

        d['info'] = list(map( lambda x: x.dump(), self.info ))

        return d

class Translation(Model):
    language = Column( Enum(LanguageCode), primary_key=True )
