from flask_restful import reqparse, Resource
from flask import request
from tree.models import Branch as BranchModel
from tree.models import BranchPost as BranchPostModel
from schematics.validate import DataError
from bson.objectid import ObjectId
import json


branch_parser = reqparse.RequestParser()
branch_parser.add_argument("name")
branch_parser.add_argument("description")
branch_parser.add_argument("parent_id")
branch_parser.add_argument("features", action="append", type=dict)


class Branch(Resource):

    def get(self, uid):
        branch = BranchModel.get(uid)
        return branch.to_output()

    def delete(self, uid):
        BranchModel.delete(uid)
        return '', 204

    def put(self, uid):
        branch = BranchModel.get(uid)

        args = branch_parser.parse_args()
        for k, v in args.items():
            setattr(branch, k, v)

        try:
            branch.validate()
        except DataError, e:
            errors = json.loads(str(e))
            return errors, 400
        else:
            branch.save()
            return branch.to_output(), 202


class BranchList(Resource):

    def get(self):
        filters = {}
        parent_id = request.args.get('parent_id')
        filters["parent_id"] = parent_id
        items = BranchModel.get_list(filters=filters)
        return items

    def post(self):
        args = branch_parser.parse_args()
        branch = BranchModel(args)
        try:
            branch.validate()
        except DataError, e:
            errors = json.loads(str(e))
            return errors, 400
        else:
            branch.save()
            return branch.to_output(), 201


branch_post_parser = reqparse.RequestParser()
branch_post_update_fields = ("branch_id", ("values", dict), "text")
for f in branch_post_update_fields:
    if type(f) is tuple:
        f, f_type = f
    else:
        f_type = str
    branch_post_parser.add_argument(f, type=f_type)


class BranchPostList(Resource):

    def get(self, branch_id):
        filters = {"branch_id": ObjectId(branch_id)}
        items = BranchPostModel.get_list(filters=filters)
        return items

    def post(self, branch_id):
        data = branch_post_parser.parse_args()
        data["branch_id"] = ObjectId(branch_id)
        post = BranchPostModel(data)
        try:
            post.validate()
        except DataError, e:
            errors = json.loads(str(e))
            return errors, 400
        else:
            post.save()
            return post.to_output(), 201
