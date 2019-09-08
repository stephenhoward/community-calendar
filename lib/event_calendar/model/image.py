from sqlalchemy.orm import relationship
from event_calendar.model import Model, ContentStatus
from sqlalchemy import Column, Text, LargeBinary, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from event_calendar.database import Base
from event_calendar.config import config
import os

class Image:
    _base_path = config.get('uploads','public')

    def __init__(self,**kwargs):
        self.filename = kwargs['filename']

    @classmethod
    def path(cls):
        return os.path.join(cls._base_path, cls._type_path )

class SiteImage(Image):
    _type_path = 'site'

    def dump(self):
        return {
            'filename': self.filename
        }

class ModelImage(Image,Model):
    _draft_path = config.get('uploads','draft')
    filename    = Column( Text )
    status      = Column( Enum(ContentStatus) )

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.status = 'Draft'

    @classmethod
    def path(cls):
        return os.path.join(cls._draft_path, cls._type_path )

    def path(self):
        if self.status == 'Draft':
            return os.path.join(self._draft_path, self._type_path )
        else:
            return os.path.join(self._base_path, self._type_path )

    def publish(self):
        if self.status == 'Draft':
            os.rename(
                os.path.join( self.path(), self.filename ),
                os.path.join( super().path(), self.filename )
            )
            self.status = 'Active'
            self.save()

class EventImage(ModelImage,Base):
    __tablename__ = 'event_images'
    _type_path    = 'events'

    event_id = Column( UUID(as_uuid=True), ForeignKey('events.id') )

class SeriesImage(ModelImage,Base):
    __tablename__ = 'series_images'
    _type_path    = 'series'

    series_id = Column( UUID(as_uuid=True), ForeignKey('series.id') )

class CategoryImage(ModelImage,Base):
    __tablename__ = 'category_images'
    _type_path    = 'categories'

    category_id = Column( UUID(as_uuid=True), ForeignKey('categories.id') )

