from sqlalchemy import Column, Table, String, Text, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from event_calendar.model import Model, Translation
from event_calendar.database import Base

class Category(Model,Base):
    __tablename__ = 'categories'

    id     = Column( UUID, primary_key=True )
    info   = relationship( "CategoryInfo", back_populates="category" )
    images = relationship( "Image" )

# for translatable parts of the event
class CategoryInfo(Translation,Base):
    __tablename__ = 'categories_i18n'

    name        = Column( Text )
    description = Column( Text )

    category = relationship( "Category", back_populates="info" )

