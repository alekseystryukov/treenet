from utils.tests import MyTestCase
from userprofile.models import UserProfile
from mock import patch
import json


class AuthTestCase(MyTestCase):
    user_info = {
        "family_name": "Stryukov",
        "name": "Aleksey Stryukov",
        "picture": "https://lh4.googleusercontent.com/-ou8xVSozKGg/AAAAAAAAAAI/AAAAAAAAD4w/CXo20rCRBdw/photo.jpg",
        "locale": "en",
        "gender": "male",
        "email": "aleksey.stryukov@gmail.com",
        "link": "https://plus.google.com/108090076208598149445",
        "given_name": "Aleksey",
        "id": "108090076208598149445",
        "verified_email": True
    }

    def setUp(self):
        self.base_url = "/auth/"

    def test_auth_get(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 403)
        self.assertIn("client_id", response.data)

    def test_auth_get_with_code(self):
        self.assertIsNone(UserProfile.objects.first())

        with patch("userprofile.api.views.get_user_info", lambda _: self.user_info):
            response = self.client.get(self.base_url + "?code=666")
        self.assertEqual(response.status_code, 200)
        user = response.data
        self.assertIsNotNone(user)
        self.assertEqual(user["name"], self.user_info["name"])
        self.assertEqual(user["picture"], self.user_info["picture"])

    def test_auth_get_with_token(self):
        self.assertIsNone(UserProfile.objects.first())
        user = UserProfile.create_from_google_info(self.user_info)

        extra = {'HTTP_AUTHORIZATION': 'Token {}'.format(user.token)}
        response = self.client.get(self.base_url, **extra)

        self.assertEqual(response.status_code, 200)
        user = response.data
        self.assertIsNotNone(user)
        self.assertEqual(user["name"], self.user_info["name"])
        self.assertEqual(user["picture"], self.user_info["picture"])

    def test_auth_patch(self):
        self.assertIsNone(UserProfile.objects.first())
        user = UserProfile.create_from_google_info(self.user_info)

        extra = {
            'HTTP_AUTHORIZATION': 'Token {}'.format(user.token),
            'CONTENT_TYPE': 'application/json',
        }
        update_data = dict(name="John Kim Chen")
        response = self.client.patch(
            self.base_url,
            json.dumps(update_data),
            **extra
        )
        self.assertEqual(response.status_code, 200)
        user = response.data
        self.assertEqual(user["name"], update_data["name"])
