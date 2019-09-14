from sqlalchemy import Column, Table, String, Text, Enum, Boolean, DateTime, ForeignKey, tuple_
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID
import enum
from event_calendar.model import TranslatableModel, Translation, ContentStatus
from event_calendar.database import Base
import event_calendar.model.image
import event_calendar.model.location
import event_calendar.model.user
from event_calendar.model.link import SeriesLink

SeriesStatus = enum.Enum( 'SeriesStatus', [
    'Draft',
    'Active'
])

class Series(TranslatableModel,Base):
    __tablename__ = 'series'

    id            = Column( UUID(as_uuid=True), primary_key=True )
    status        = Column( Enum(ContentStatus) )
    contact_phone = Column( String )
    contact_email = Column( String )

    urls       = relationship( "SeriesLink" )
    info       = relationship( "SeriesInfo", lazy='joined' )
    images     = relationship( "SeriesImage" )
    events     = relationship( "Event", back_populates="series" )
    comments   = relationship( "SeriesComment", back_populates="series" )

# for translatable parts of the event
class SeriesInfo(Translation,Base):
    __tablename__ = 'series_i18n'

    id          = Column( UUID(as_uuid=True), ForeignKey('series.id'), primary_key=True )
    title       = Column( Text )
    description = Column( Text )
    accessibility_information = Column( Text )

    event = relationship( "Series" )
