import enum
from sqlalchemy import Column, String, Table, ForeignKey, Enum, Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as UUIDColumn
from uuid import UUID, uuid4 as uuid
from event_calendar.model import Model
from event_calendar.database import Base, DB

db = DB()

UserRoleEnum = enum.Enum( 'UserRoleEnum', [
    'Contributor',
    'Editor',
    'Administrator'
])

class RoleError(Exception):
    pass

class UserRole(Base):
    __tablename__ = 'user_roles'
    id = Column( UUIDColumn(as_uuid=True), primary_key=True )
    org_id  = Column( UUIDColumn(as_uuid=True), ForeignKey('orgs.id') )
    user_id = Column( UUIDColumn(as_uuid=True), ForeignKey('users.id') )
    role    = Column( Enum(UserRoleEnum) )

    Index(
        "uix_user_role_org",
        "org_id",
        "user_id",
        "role",
        unique=True,
        postgresql_where=org_id.isnot(None)
    ),
    Index(
        "uix_user_role",
        "user_id",
        "role",
        unique=True,
        postgresql_where=org_id.is_(None)
    )

    org  = relationship('Org', backref="user_roles")
    user = relationship('User', back_populates="roles")

    @classmethod
    def create(cls,dict):
        role = cls(**dict)

        if ( not isinstance( role.id, UUID ) ):
            role.id = uuid()

        db.session.add(role)
        return role

class Org(Model,Base):
    __tablename__ = 'orgs'

    name  = Column( String )
    users = relationship('User', secondary='user_roles' )