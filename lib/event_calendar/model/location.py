from sqlalchemy.orm import relationship
from event_calendar.model import TranslatableModel, Translation
from sqlalchemy import Column, Text, LargeBinary, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from event_calendar.database import Base

class Location(TranslatableModel,Base):
    __tablename__ = 'locations'

    address1 = Column( String )
    address2 = Column( String )
    city     = Column( String )
    state    = Column( String )
    postal_code = Column( String )
    info = relationship( "LocationInfo", lazy='joined' )

class LocationInfo(Translation,Base):
    __tablename__ = 'location_i18n'

    id          = Column( UUID(as_uuid=True), ForeignKey('locations.id'), primary_key=True )
    name        = Column( Text )
    description = Column( Text )
    accessibility_information = Column( Text )
