"""Tests for plugin.py."""
import time

import httpretty
import jwt
import requests
import authorization_levels

# import ckan.plugins as plugins


def token_default():
    """
    Mock JWT payload of an access token response
    """
    now = int(time.time())
    lifetime = 10
    return jwt.encode({'iat': now, 'exp': now + lifetime, 'authz': authorization_levels.LEVEL_DEFAULT}, 'secret', algorithm='HS256')


def token_employee():
    """
    Mock JWT payload of an access token response
    """
    now = int(time.time())
    lifetime = 10
    return jwt.encode({'iat': now, 'exp': now + lifetime, 'authz': authorization_levels.LEVEL_EMPLOYEE}, 'secret', algorithm='HS256')


def token_employee_plus():
    """
    Mock JWT payload of an access token response
    """
    now = int(time.time())
    lifetime = 10
    return jwt.encode({'iat': now, 'exp': now + lifetime, 'authz': authorization_levels.LEVEL_EMPLOYEE_PLUS}, 'secret', algorithm='HS256')


def _access_token_response_dict(payload):
    """
    Mock values for an access token response.
    """
    params = {}
    params['access_token'] = 'fake access token'
    params['refresh_token'] = 'fake refesh token'
    params['expires_on'] = 'fake expires on'
    params['id_token'] = jwt.encode(payload, params['access_token'])
    return params


@httpretty.activate
def test_login():
    endpoint = "http://datapunt.amsterdam.nl/catalogus/login_generic"
    httpretty.register_uri(httpretty.POST, endpoint, body="logged in")
    response = requests.post(endpoint)
    assert response.text == "logged in"
