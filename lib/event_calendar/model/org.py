import enum
from sqlalchemy import Column, String, Table, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from event_calendar.model import Model
from event_calendar.database import Base

UserRole = enum.Enum( 'UserRole', [
    'Contributor',
    'Editor',
    'Administrator'
])

users_orgs_table = Table('users_orgs', Base.metadata,
    Column('org_id',  UUID(as_uuid=True), ForeignKey('orgs.id')),
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id')),
    Column('role',    Enum(UserRole) )
)

class Org(Model,Base):
    __tablename__ = 'orgs'

    name  = Column( String )
    users = relationship('User', secondary=users_orgs_table, backref='orgs' )