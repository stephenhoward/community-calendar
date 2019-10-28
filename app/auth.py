from flask import jsonify, request, g, abort, make_response, current_app as app
from werkzeug.exceptions import Unauthorized
from event_calendar.model.user import User
from event_calendar.model.password_token import PasswordToken
from event_calendar.site_settings import site_settings
import jwt
import time
from event_calendar.config import config

JWT_ISSUER           = 'com.events-calendar.api'
JWT_LIFETIME_SECONDS = 600

def create_password_token():

    email = request.json['email'].lower()
    user  = User.search( User.email == email ).first()

    if user:
        token = PasswordToken.generate(user)
        token.send()

    return 'Ok'

def verify_password_token(id):

    token = PasswordToken.retrieve(id)

    if token:
        return 'Ok'

    abort( make_response( 'NoTokenFound', 404 ) )

def use_password_token(id):

    token = PasswordToken.retrieve(id)

    if token:
        user = token.user;

        user.set_password(request.json['password'])
        user.save()
        token.delete()
        return 'Ok'

    abort( make_response( 'NoTokenFound', 404 ) )

def get_token():

    email = request.json['email'].lower()

    if site_settings.needs_setup:
        return _generate_token( User(email = email) )

    user = User.search( User.email == email ).first()

    if user:
        if user.check_password( request.json['password'] ):
            return _generate_token(user)

    abort( make_response( 'UnknownLogin',401 ) )

def refresh_token():

    if g.claims:
        user = User.get( g.claims['id'] )
        if user:
            return _generate_token(user)

    abort( make_response( 'Invalid token, cannot refresh',401 ) )

def decode_token(token):
    try:
        g.claims = jwt.decode(token, app.config['JWT_PUBLIC_KEY'], algorithms='RS256')
        g.user   = User.get( g.claims['id'] )
        return g.claims
    except jwt.exceptions.InvalidTokenError as e:
        abort( make_response('InvalidToken', 401) )

def _generate_token(user):

    timestamp = int(time.time())
    claims = {
        "iss":   JWT_ISSUER,
        "iat":   int(timestamp),
        "exp":   int(timestamp + JWT_LIFETIME_SECONDS),
        "id":    str(user.id),
    }

    if site_settings.needs_setup == 1:
        claims['setup_only'] = 1

    return jwt.encode(claims, app.config['JWT_PRIVATE_KEY'], algorithm='RS256').decode('ascii')

