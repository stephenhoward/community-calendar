from event_calendar.model import Model
from event_calendar.model.content import Content
from sqlalchemy import Column, Text
from event_calendar.database import Base
from event_calendar.config import config
import os

class BaseImage(object):
    _base_path = config.get('uploads','public')

    def __init__(self,**kwargs):
        self.filename = kwargs['filename']

    @classmethod
    def path(cls):
        return os.path.join(cls._base_path, cls._type_path )

class SiteImage(BaseImage):
    _type_path = 'site'

    def dump(self):
        return {
            'filename': self.filename
        }

class Image(BaseImage,Content,Model,Base):
    __tablename__ = 'images'
    _draft_path = config.get('uploads','draft')
    _type_path    = 'events'
    filename    = Column( Text )

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
