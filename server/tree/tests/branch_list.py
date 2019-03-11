from utils.test import MainTestCase
from tree.models import Branch


class BranchesListTestCase(MainTestCase):

    def test_empty_list(self):
        response = self.app.get('/branches')
        assert response.status_code == 200
        assert len(response.json) == 0, "List is empty"

    def test_top_level_list(self):
        branch = Branch(dict(name="Hello"))
        branch.save()

        response = self.app.get('/branches')
        assert response.status_code == 200
        assert len(response.json) == 1
        item = response.json[0]
        assert item["id"] == str(branch.id)

    def test_sub_list(self):
        top_branch = Branch(dict(name="Hello"))
        top_branch.save()

        sub_branch = Branch(dict(name="Hi", parent_id=top_branch.id))
        sub_branch.save()

        response = self.app.get('/branches?parent_id={}'.format(top_branch.id))
        assert response.status_code == 200
        assert len(response.json) == 1
        item = response.json[0]
        assert item["id"] == str(sub_branch.id)

    def test_post_branch(self):
        post_data = {
            "name": "Sport",
            "parent_id": "f" * 24,
        }
        response = self.app.post(
            '/branches',
            data=post_data
        )
        assert response.status_code == 201
        data = response.json
        assert data["name"] == post_data["name"]
        assert data["parent_id"] == post_data["parent_id"]

    def test_fail_short_name(self):
        response = self.app.post(
            '/branches',
            data={"name": "S"}
        )
        assert response.status_code == 400
        data = response.json
        assert "name" in data
        assert data["name"] == ["String value is too short."]
