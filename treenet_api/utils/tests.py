from django.test import TestCase
from django.conf import settings
from userprofile.models import UserProfile


class MyTestCase(TestCase):
    def tearDown(self):
        settings.MY_DB_CONN.drop_database(settings.MY_TEST_DB_NAME)

    def auth_user(self):
        user = UserProfile(name="Test user", google_email="e@gmail.com")
        user.save()
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Token {}'.format(user.token)
