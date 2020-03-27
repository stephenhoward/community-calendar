from sqlalchemy.orm import relationship
from event_calendar.model.content import PrimaryContentModel, TranslationModel
from sqlalchemy import Column, Text, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from event_calendar.database import Base

class Location(PrimaryContentModel,Base):
    __tablename__ = 'locations'

    address1 = Column( String )
    address2 = Column( String )
    city     = Column( String )
    state    = Column( String )
    postal_code = Column( String )
    info = relationship( "LocationInfo", lazy='joined' )

class LocationInfo(TranslationModel,Base):
    __tablename__ = 'locations_i18n'

    id          = Column( UUID(as_uuid=True), ForeignKey('locations.id'), primary_key=True )
    name        = Column( Text )
    description = Column( Text )
    accessibility_information = Column( Text )
