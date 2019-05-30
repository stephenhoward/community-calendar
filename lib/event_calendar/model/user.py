from sqlalchemy import Column, Table, String, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from event_calendar.model import Model, Translation
from event_calendar.database import Base

UserRole = enum.Enum( 'UserRole', [
    'Contributor',
    'Editor',
    'Administrator'
])

class User(Model,Base):
    __tablename__ = 'users'

    role  = Column( Enum(UserRole) )
    email = Column( String )
