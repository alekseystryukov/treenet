from utils.tests import MyTestCase
from tree.models import Branch


class BranchesListTestCase(MyTestCase):

    def test_fail_access(self):
        response = self.client.get('/branches/')
        self.assertEqual(response.status_code, 401)

    def test_empty_list(self):
        self.auth_user()
        response = self.client.get('/branches/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0, "List is empty")

    def test_top_level_list(self):
        self.auth_user()
        branch = Branch(name="Hello")
        branch.save()

        response = self.client.get('/branches/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], str(branch.id))

    def test_sub_list(self):
        self.auth_user()

        top_branch = Branch(name="Hello")
        top_branch.save()

        sub_branch = Branch(name="Hi there", parent_id=top_branch.id)
        sub_branch.save()

        response = self.client.get('/branches/?parent_id={}'.format(top_branch.id))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], str(sub_branch.id))

    def test_post_branch(self):
        self.auth_user()

        post_data = {
            "name": "Sport",
            "parent_id": "f" * 24,
        }
        response = self.client.post(
            '/branches/',
            data=post_data
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["name"], post_data["name"])

        branch = Branch.objects.get(id=data["id"])
        self.assertEqual(str(branch.parent_id), post_data["parent_id"])

    def test_fail_short_name(self):
        self.auth_user()
        response = self.client.post(
            '/branches/',
            data={"name": "S"}
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("name", data)
        self.assertEqual(data["name"], ["Ensure this field has at least 3 characters."])