from event_calendar.config import config
from event_calendar.model.user import User
from event_calendar.model.org import Org, RoleError
from event_calendar.database import DB
import unittest

db = DB()

test_user = {
    "email": "roles@example.com",
    "password": "baddpassword"
}

class TestAPI(unittest.TestCase):

    def setUp(self):
        config.set(['db','database'],'test_roles')
        db.build_engine()
        db.create_db()

    def tearDown(self):
        db.destroy_db()

    def test_roles(self):
        org  = Org.create({ "name": "Acme" }).save()
        org2 = Org.create({ "name": "Emca" }).save()
        user = User.create(test_user).save()

        user.grant_role( 'Contributor', for_org=org )

        self.assertRaises( Exception, user.has_role, 'Contributor' )
        self.assertRaises( RoleError, user.has_role, 'BadRoleName',   for_org=org )
        assert( user.has_role('Contributor',   for_org=org2) == False )
        assert( user.has_role('Administrator', for_org=org)  == False )
        assert( user.has_role('Contributor', for_org=org)    == True )

if __name__ == '__main__':
    unittest.main()
