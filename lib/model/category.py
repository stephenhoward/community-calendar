from sqlalchemy import Column, Table, Text, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

class Category(Base):
    __tablename__ = 'categories'

    id     = Column( UUID, primary_key=True )
    info   = relationship( "CategoryInfo", back_popluates="category" )
    images = relationship( "Image" )

# for translatable parts of the event
class CategoryInfo(Base):
    __tablename__ = 'events_i18n'

    id          = Column( UUID,    primary_key=True, ForeignKey('categories.id') )
    language    = Column( VarChar, primary_key=True )
    name        = Column( Text )
    description = Column( Text )

    category = relationship( "Category", back_populates="info" )

