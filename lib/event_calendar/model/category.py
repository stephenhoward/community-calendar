from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from event_calendar.model import Model
from event_calendar.model.content import TranslatableMixin, TranslationModel
from event_calendar.database import Base

class Category(TranslatableMixin,Model,Base):
    __tablename__ = 'categories'

    info   = relationship( "CategoryInfo", lazy='joined' )
    image  = Column( String )

# for translatable parts of the event
class CategoryInfo(TranslationModel,Base):
    __tablename__ = 'categories_i18n'

    id          = Column( UUID(as_uuid=True), ForeignKey('categories.id'), primary_key=True )
    name        = Column( Text )
    description = Column( Text )

    category = relationship( "Category" )

