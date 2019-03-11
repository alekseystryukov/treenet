from flask_restful import reqparse, Resource
from urllib import urlencode
import requests
from flask import request
from schematics.validate import DataError
import json


BASE_URL = 'https://accounts.google.com/o/oauth2/'
AUTH_URL = BASE_URL + 'auth'
TOKEN_URL = BASE_URL + 'token'
USER_INFO_URL = 'https://www.googleapis.com/oauth2/v2/userinfo'
GOOGLE_CLIENT_ID = '138430851207-deb2edrpcbrssfp9a62netfot4h53mfn.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '3P5V2HzA5G49NJ9ZO8hv0Mr0'
REDIRECT_URI = 'http://treenet.com:3000/auth'  # one of the Redirect URIs from Google APIs console

AUTH_PARAMS = {
    "response_type": "code",
    "client_id": GOOGLE_CLIENT_ID,
    "redirect_uri": REDIRECT_URI,
    "scope": "https://www.googleapis.com/auth/userinfo.profile"
}

TOKEN_PARAMS = {
    "client_id": GOOGLE_CLIENT_ID,
    "client_secret": GOOGLE_CLIENT_SECRET,
    "redirect_uri": REDIRECT_URI,
    "grant_type": "authorization_code",
}


parser = reqparse.RequestParser()
parser.add_argument("auth_token")


class Auth(Resource):

    def get(self):
        code = request.args.get('code')
        if code:
            TOKEN_PARAMS["code"] = code
            content_length = len(urlencode(TOKEN_PARAMS))
            TOKEN_PARAMS['content-length'] = str(content_length)
            r = requests.post(TOKEN_URL, data=TOKEN_PARAMS)
            data = r.json()
            print(data)

            # get user data
            access_token = data['access_token']
            headers = {"Authorization": "OAuth %s" % access_token}
            data = requests.get(USER_INFO_URL, headers=headers)
            return data.json()
        else:
            url = "{}?{}".format(AUTH_URL, urlencode(AUTH_PARAMS))
            return {"google": url}, 403

    def post(self):
        return '', 201
