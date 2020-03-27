from sqlalchemy import Column, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from event_calendar.model.content import PrimaryContentModel, TranslationModel
from event_calendar.database import Base

class Series(PrimaryContentModel,Base):
    __tablename__ = 'series'

    info       = relationship( "SeriesInfo", lazy='joined' )

# for translatable parts of the event
class SeriesInfo(TranslationModel,Base):
    __tablename__ = 'series_i18n'

    id          = Column( UUID(as_uuid=True), ForeignKey('series.id'), primary_key=True )
    title       = Column( Text )
    description = Column( Text )
    accessibility_information = Column( Text )

    series = relationship( "Series" )
