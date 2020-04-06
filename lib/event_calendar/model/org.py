import enum
from sqlalchemy import Column, String, Table, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from event_calendar.model import Model
from event_calendar.database import Base

UserRoleEnum = enum.Enum( 'UserRoleEnum', [
    'Contributor',
    'Editor',
    'Administrator'
])

class RoleError(Exception):
    pass

class UserRole(Base):
    __tablename__ = 'user_roles'
    org_id  = Column( UUID(as_uuid=True), ForeignKey('orgs.id'), primary_key = True)
    user_id = Column( UUID(as_uuid=True), ForeignKey('users.id'), primary_key = True)
    role    = Column( Enum(UserRoleEnum) )

    org  = relationship('Org', backref="user_roles")
    user = relationship('User', back_populates="roles")

class Org(Model,Base):
    __tablename__ = 'orgs'

    name  = Column( String )
    users = relationship('User', secondary='user_roles' )