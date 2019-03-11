from utils.test import MainTestCase
from tree.models import Branch


class BranchPostTestCase(MainTestCase):

    def test_post(self):
        branch = Branch(dict(
            name="Hello",
            features=[
                {"name": "distance", "representation": "number"}
            ],
        ))
        branch.save()

        create_data = {
            "text": "run 12km this morning. got tired",
            "values": {
                "distance": 12000,
            }
        }
        response = self.app.post(
            '/branch/{}/posts'.format(branch._id),
            data=create_data
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)

    def test_post_error(self):
        branch = Branch(dict(
            name="Hello",
            features=[
                {"name": "distance", "representation": "number"}
            ],
        ))
        branch.save()

        create_data = {
            "text": "run 12km this morning. got tired",
            "values": {
                "distance": "twenty feets",
            }
        }
        response = self.app.post(
            '/branch/{}/posts'.format(branch._id),
            data=create_data
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("values", response.json)
