import os
import enum
import yaml
import base64
import cryptography.exceptions
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
from sqlalchemy import Column, String, Binary, Enum, or_
import event_calendar.model.org
from sqlalchemy.orm import relationship
from event_calendar.model import Model
from event_calendar.database import Base
from event_calendar.model.org import Org, UserRole, UserRoleEnum, RoleError

codes = yaml.load( open('config/languages.yaml','r'), Loader=yaml.FullLoader )

LanguageCode  = enum.Enum( 'LanguageCode', list(codes.keys()) )

class User(Model,Base):
    __tablename__ = 'users'

    email    = Column( String, unique=True )
    language = Column( Enum(LanguageCode), default='en' )
    name     = Column( String )
    salt     = Column( Binary )
    password = Column( Binary )
    orgs     = relationship('Org', secondary='user_roles')
    roles    = relationship('UserRole', back_populates="user", lazy="dynamic")

    def _dont_dump(self):
        return ['salt','password'];

    def update_attr(self,attr,value):
        if attr not in self._dont_dump():
            setattr( self, attr, value )
        elif attr == 'password':
            self.set_password(value)

    def __init__(self,**kwargs):

        password = kwargs.pop('password', None)

        if kwargs['email']:
            kwargs['email'] = kwargs['email'].lower()

        super().__init__(**kwargs)

        if password is not None:
            self.set_password(password)

    def check_password(self,clear_password):

        if clear_password is None or len(clear_password) == 0:
            return False

        if ( self.salt and self.password ):

            kdf = self._new_scrypt( base64.b64decode( self.salt ) )

            try:
                kdf.verify( clear_password.encode('utf-8'), base64.b64decode(self.password) )
                return True
            except cryptography.exceptions.InvalidKey:
                return False

        return False

    def set_password(self,password):

        salt    = os.urandom(16)
        kdf     = self._new_scrypt(salt)

        self.salt     = base64.b64encode( salt )
        self.password = base64.b64encode( kdf.derive( password.encode('utf-8') ) )

    def _new_scrypt(self,salt):

        backend = default_backend()

        return Scrypt( salt=salt, length=32, n=2**14, r=8, p=1, backend=backend )

    def has_role(self,role, **kwargs ):

        if 'for_org' not in kwargs:
            raise Exception( 'User.has_role requires org or org_id parameter "for_org"' )

        if role not in UserRoleEnum.__members__:
            raise RoleError( 'No such role "' + role )

        if kwargs['for_org'] is None:
            roles = self.roles.filter( UserRole.role == role, UserRole.org_id == None )
        else:
            org_id = kwargs['for_org'].id if isinstance(kwargs['for_org'],Org) else kwargs['for_org']
            roles  = self.roles.filter( UserRole.role == role, or_( UserRole.org_id == org_id,  UserRole.org_id == None ) ).all()

        return True if len(roles) > 0 else False

    def grant_role(self,role,**kwargs):

        if 'for_org' not in kwargs:
            raise Exception( 'User.has_role requires org or org_id parameter "for_org"' )

        if role not in UserRoleEnum.__members__:
            raise RoleError( 'No such role "' + role )

        org = kwargs['for_org'] if ( isinstance(kwargs['for_org'],Org) ) else Org.get(kwargs['for_org'])

        if org is None:
            raise Exception('Org "' + kwargs['for_org'] + '" not found')

        self.roles.append(UserRole(
            user_id = self.id,
            org_id = org.id,
            role = UserRoleEnum[role]
        ))
        self.save()

        return True
