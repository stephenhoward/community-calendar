from sqlalchemy import Column, Enum, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects.postgresql import UUID
from event_calendar.model import Model
from event_calendar.model.comment import CommentableMixin
from event_calendar.database import DB,Base
import enum
import yaml

db    = DB()
codes = yaml.load( open('config/languages.yaml','r'), Loader=yaml.FullLoader )

LanguageCode  = enum.Enum( 'LanguageCode', list(codes.keys()) )
ContentStatus = enum.Enum( 'ContentStatus', [
    'Draft',
    'Active'
])

content_images_table = Table('content_images', Base.metadata,
    Column('id',    UUID(as_uuid=True) ),
    Column('image_id', UUID(as_uuid=True), ForeignKey('images.id'))
)

content_links_table = Table('content_links', Base.metadata,
    Column('id',    UUID(as_uuid=True) ),
    Column('link_id', UUID(as_uuid=True), ForeignKey('links.id'))
)

class ContactMixin(object):
    contact_phone = Column( String )
    contact_email = Column( String )

class ContentMixin(object):

    org_id = Column( UUID(as_uuid=True) )
    status = Column( Enum(ContentStatus) )

    @declared_attr
    def org(cls):
        return relationship('Org')

class TranslatableMixin(object):

    def dump(self):
        d = super().dump()

        d['info'] = list(map( lambda x: x.dump(), self.info ))

        return d

class TranslationModel(Model):
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

class PrimaryContentModel( Model, ContentMixin, ContactMixin, CommentableMixin, TranslatableMixin ):

    @declared_attr
    def urls(cls):
        return relationship( "Link", secondary = content_links_table )

    @declared_attr
    def images(cls):
        return relationship( "Image", secondary = content_images_table )
