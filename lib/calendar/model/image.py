from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from calendar.model import Model, Translation
from sqlalchemy import Column, Text, LargeBinary

Base = declarative_base()

class Image(Model,Base):
    __tablename__ = 'images'

    data = Column( LargeBinary )
    info = relationship( "ImageInfo", back_populates="image")

class ImageInfo(Translation,Base):
    __tablename__ = 'image_info'

    title       = Column( Text )
    description = Column( Text )