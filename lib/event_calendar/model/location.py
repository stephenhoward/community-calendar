from sqlalchemy.orm import relationship
from event_calendar.model import Model, Translation
from sqlalchemy import Column, Text, LargeBinary, String
from event_calendar.database import Base

class Location(Model,Base):
    __tablename__ = 'location'

    address1 = Column( String )
    address2 = Column( String )
    city     = Column( String )
    state    = Column( String )
    postal_code = Column( String )
    info = relationship( "LocationInfo" )

class LocationInfo(Translation,Base):
    __tablename__ = 'location_i18n'

    name        = Column( Text )
    description = Column( Text )
    accessibility_information = Column( Text )
