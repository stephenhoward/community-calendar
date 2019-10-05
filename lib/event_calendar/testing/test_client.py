from flask.testing import FlaskClient
from event_calendar.model.user import User
from werkzeug.datastructures import Headers

test_user = {
    "email": "test@example.com",
    "password": "baddpassword"
}

class TestClient(FlaskClient):

    auth_token = None

    def login(self):
        user = User.create(test_user)
        user.save()

        res = self.post('/v1/auth/token', json = test_user )
        self.auth_token = res.data.decode('ascii')

        return res

    def open(self, *args, **kwargs):

        if self.auth_token:
            auth_headers = {
                'Authorization': 'Bearer ' + self.auth_token
            }
            headers = kwargs.pop('headers',{})
            headers.update(auth_headers)
            kwargs['headers'] = headers

        return super().open(*args, **kwargs)