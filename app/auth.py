from flask import jsonify, request, g, abort, make_response, current_app as app
from werkzeug.exceptions import Unauthorized
from event_calendar.model.user import User
import jwt
import time

JWT_ISSUER = 'com.zalando.connexion'
JWT_LIFETIME_SECONDS = 600

def get_token():

    user = User.search( email = request.json['email'].lower() ).first()

    if user:
        if user.check_password( request.json['password'] ):
            return _generate_token(user)

    abort( make_response( 'Unknown user or password',401 ) )

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
        abort( make_response('Invalid Token', 401) )

def _generate_token(user):

    timestamp = int(time.time())
    claims = {
        "iss":   JWT_ISSUER,
        "iat":   int(timestamp),
        "exp":   int(timestamp + JWT_LIFETIME_SECONDS),
        "id":    str(user.id),
    }

    return jwt.encode(claims, app.config['JWT_PRIVATE_KEY'], algorithm='RS256').decode('ascii')

