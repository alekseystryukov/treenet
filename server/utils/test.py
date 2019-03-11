from flask.testing import FlaskClient
from flask.wrappers import Response
from tree.main import app
from tree.models import QueryModel
import logging
import unittest
import json

logging.basicConfig()
logger = logging.getLogger(__name__)


class JSONResponseWrapper(Response):

    @property
    def json(self):
        return json.loads(self.data)


class TestClient(FlaskClient):

    def open(self, *args, **kwargs):
        if 'data' in kwargs:
            kwargs['data'] = json.dumps(kwargs.pop('data'))
            kwargs['content_type'] = 'application/json'
        return super(TestClient, self).open(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(TestClient, self).__init__(
            args[0],
            response_wrapper=JSONResponseWrapper,
            **kwargs
        )


class MainTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        print(app.testing)
        app.test_client_class = TestClient
        self.app = app.test_client()

    def tearDown(self):
        for c in QueryModel.collections.values():
            if not c.name.startswith("TEST_"):
                logger.error(
                    "tearDown: Skip collection {} from dropping".format(c.name)
                )
                continue

            c.drop()
