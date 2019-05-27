from sqlalchemy.orm import relationship
from event_calendar.model import Model, Translation
from sqlalchemy import Column, Text, LargeBinary
from event_calendar.database import Base

class Image(Model,Base):
    __tablename__ = 'images'

    data = Column( LargeBinary )
    info = relationship( "ImageInfo", back_populates="image")

class ImageInfo(Translation,Base):
    __tablename__ = 'image_i18n'

    title       = Column( Text )
    description = Column( Text )