from sqlalchemy import Column, Enum, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects.postgresql import UUID
from event_calendar.model import Model
from event_calendar.model.org import Org
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

class Content(object):

    status = Column( Enum(ContentStatus) )

    @declared_attr
    def org_id(cls):
        return Column( UUID(as_uuid=True), ForeignKey('orgs.id') )

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


class PrimaryContentModel( Model, Content, CommentableMixin, TranslatableMixin ):

    contact_phone = Column( String )
    contact_email = Column( String )

    @declared_attr
    def urls(cls):
        from event_calendar.model.link import Link
        content_links_table = Base.metadata.tables['content_links'] \
            if 'content_links' in Base.metadata.tables \
            else Table('content_links', Base.metadata,
                Column('id',    UUID(as_uuid=True) ),
                Column('link_id', UUID(as_uuid=True), ForeignKey('links.id'))
            )
        return relationship( "Link", secondary = content_links_table, primaryjoin= ( cls.__name__ + ".id == content_links.c.id" ) )

    @declared_attr
    def images(cls):
        from event_calendar.model.image import Image
        content_images_table = Base.metadata.tables['content_images'] \
            if 'content_images' in Base.metadata.tables \
            else Table('content_images', Base.metadata,
                Column('id',    UUID(as_uuid=True) ),
                Column('image_id', UUID(as_uuid=True), ForeignKey('images.id'))
            )
        return relationship( "Image", secondary = content_images_table, primaryjoin= ( cls.__name__ + ".id == content_images.c.id" ) )
