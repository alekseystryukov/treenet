from utils.tests import MyTestCase
from tree.models import Branch
import json


class BranchTestCase(MyTestCase):

    def test_update(self):
        self.auth_user()

        branch = Branch(name="Hello")
        branch.save()

        update_data = {
            "name": "Sport",
            "parent_id": "f" * 24,
            "features": [{"name": "Hours", "representation": "number"}],
        }
        response = self.client.put('/branch/{}/'.format(branch.id),
                                   data=json.dumps(update_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data["id"], str(branch.id))
        self.assertEqual(data["name"], update_data["name"])
        self.assertEqual(data["parent_id"], update_data["parent_id"])
        self.assertEqual(len(data["features"]), 1)
        self.assertEqual(data["features"][0]["name"],
                         update_data["features"][0]["name"])
        self.assertEqual(data["features"][0]["representation"],
                         update_data["features"][0]["representation"])

    def test_update_error(self):
        self.auth_user()

        branch = Branch(name="Hello")
        branch.save()

        update_data = {"name": "S"}
        response = self.client.put('/branch/{}/'.format(branch.id),
                                   data=json.dumps(update_data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("name", response.json())

    def test_access_error(self):
        branch = Branch(name="Hello")
        branch.save()

        update_data = {"name": "New name"}
        response = self.client.put('/branch/{}/'.format(branch.id),
                                   data=json.dumps(update_data), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["detail"], "Authentication credentials were not provided.")
