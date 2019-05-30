from sqlalchemy.orm import relationship
from event_calendar.model import Model, Translation
from sqlalchemy import Column, Text, LargeBinary, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from event_calendar.database import Base

class Image(Model,Base):
    __tablename__ = 'images'

    data = Column( LargeBinary )
    info = relationship( "ImageInfo" )

class EventImage(Image):

    event_id = Column( UUID(as_uuid=True), ForeignKey('events.id') )

class CategoryImage(Image):

    category_id = Column( UUID(as_uuid=True), ForeignKey('categories.id') )

class ImageInfo(Translation,Base):
    __tablename__ = 'image_i18n'

    id          = Column( UUID(as_uuid=True), ForeignKey('images.id'), primary_key=True )
    title       = Column( Text )
    description = Column( Text )