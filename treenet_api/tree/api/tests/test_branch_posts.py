from utils.tests import MyTestCase
from tree.models import Branch
import json


class BranchPostTestCase(MyTestCase):

    def test_post(self):
        self.auth_user()
        branch = Branch(
            name="Hello",
            features=[
                {"name": "distance", "representation": "number"}
            ],
        )
        branch.save()

        create_data = {
            "text": "run 12km this morning. got tired",
            "values": {
                "distance": 12000,
            }
        }
        response = self.client.post(
            '/branch/{}/posts/'.format(branch.id),
            data=json.dumps(create_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())

    def test_post_error(self):
        self.auth_user()
        branch = Branch(
            name="Hello",
            features=[
                {"name": "distance", "representation": "number"}
            ],
        )
        branch.save()

        create_data = {
            "text": "run 12km this morning. got tired",
            "values": {
                "distance": "twenty feet",
            }
        }
        response = self.client.post(
            '/branch/{}/posts/'.format(branch.id),
            data=json.dumps(create_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("values", response.json())
