from sqlalchemy.orm import relationship
from event_calendar.model import Model, Translation
from sqlalchemy import Column, Text, LargeBinary, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from event_calendar.database import Base

class Image(Model):
    filename = Column( Text )

class EventImage(Image,Base):
    __tablename__ = 'event_images'

    event_id = Column( UUID(as_uuid=True), ForeignKey('events.id') )

class SeriesImage(Image,Base):
    __tablename__ = 'series_images'

    series_id = Column( UUID(as_uuid=True), ForeignKey('series.id') )

class CategoryImage(Image,Base):
    __tablename__ = 'category_images'

    category_id = Column( UUID(as_uuid=True), ForeignKey('categories.id') )

