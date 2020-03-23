from sqlalchemy import Column, Enum
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.dialects.postgresql import UUID as UUIDColumn
from event_calendar.database import DB
from sqlalchemy.orm.exc import NoResultFound
import enum
import yaml
from uuid import UUID, uuid4 as uuid
from datetime import datetime

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
    def search(cls,*parameters):
        return cls.query.filter( *parameters )

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

        mapper = inspect( type(self) )

        for key, value in dict.items():

            attr = mapper.attrs[key]

            if isinstance( attr, RelationshipProperty ):
                if attr.uselist:
                    self.update_to_many( key, value )
                else: 
                    self.update_to_one( key, value )
            else:
                self.update_attr( key, value )

        return self

    def update_to_many(self,key,value):

        attr      = getattr( self, key )
        mapper    = inspect(type(self))
        other_cls = mapper.attrs[key].mapper.class_

        for v in value:
            for member in attr:
                if member == v:
                    if type(v) is dict:
                        member.update(v)
                    break
            else:
                new_member = None

                if isinstance(v, other_cls):
                    new_member = v
                if type(v) is str:
                    new_member = other_cls.get(v)
                    if new_member is None:
                        raise Exception( 'no ' + type(other_cls) + ' exists with identifier "' + v + '"' )
                elif type(v) is dict:
                    new_member = other_cls.create(v)

                attr.append( new_member )

        setattr( self, key, attr )

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

    def __eq__(self,other):
        if isinstance( other, type(self) ):
            return self.id == other.id
        elif type(other) is dict:
            return self.id == other['id']
        elif type(other) is str:
            return self.id == other
        else:
            return False

    def dump(self):
        dumped  = {}
        no_dump = self._dont_dump()

        for c in self.__table__.columns:
            if c.name not in no_dump:
                dumped[c.name] = getattr(self,c.name)
                if isinstance(dumped[c.name],datetime):
                    dumped[c.name] = dumped[c.name].strftime('%Y-%m-%d %H:%M')

        return dumped

    def __hash__(self):
        return hash(self.id)

class TranslatableModel(Model):

    def dump(self):
        d = super().dump()

        d['info'] = list(map( lambda x: x.dump(), self.info ))

        return d

class Translation(Model):
    language = Column( Enum(LanguageCode), primary_key=True )

    def __eq__(self,other):
        if isinstance( other, Translation ):
            return self.language == other.language
        elif type(other) is dict:
            return self.language.name == other['language']
        else:
            return False

    def _dont_dump(self):
        return ['id'];

class CommentableModel (Model):

    def get_comments(self):
        return Comment.search(
            target_class == self.__class__.__name__,
            target_id    == self.id
        ).all()

    def add_comment(self,json):
        if ( json['parent_id'] ):
            reply = Reply.create(json).save()
            return reply
        else:
            comment = Comment.create(json).save()
            self.comments.add(comment)
            return comment
