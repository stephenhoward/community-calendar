from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Table, String, Text, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from calendar.model import Model, Translation

Base = declarative_base()

class Category(Model,Base):
    __tablename__ = 'categories'

    id     = Column( UUID, primary_key=True )
    info   = relationship( "CategoryInfo", back_populates="category" )
    images = relationship( "Image" )

# for translatable parts of the event
class CategoryInfo(Translation,Base):
    __tablename__ = 'events_i18n'

    name        = Column( Text )
    description = Column( Text )

    category = relationship( "Category", back_populates="info" )

