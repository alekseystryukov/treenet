from utils.test import MainTestCase
from tree.models import Branch


class BranchTestCase(MainTestCase):

    def test_update(self):
        branch = Branch(dict(
            name="Hello",
        ))
        branch.save()

        update_data = {
            "name": "Sport",
            "parent_id": "f" * 24,
            "features": [{"name": "Hours", "representation": "number"}],
        }
        response = self.app.put(
            '/branch/{}'.format(branch._id),
            data=update_data
        )
        assert response.status_code == 202
        data = response.json
        assert data["id"] == str(branch.id)
        assert data["name"] == update_data["name"]
        assert data["parent_id"] == update_data["parent_id"]
        self.assertEqual(len(data["features"]), 1)
        self.assertEqual(data["features"][0]["name"],
                         update_data["features"][0]["name"])
        self.assertEqual(data["features"][0]["representation"],
                         update_data["features"][0]["representation"])

    def test_update_error(self):
        branch = Branch(dict(name="Hello"))
        branch.save()

        update_data = {"name": "S"}
        response = self.app.put(
            '/branch/{}'.format(branch._id),
            data=update_data
        )
        assert response.status_code == 400
        assert "name" in response.json
