from flask import Flask
from flask_restful import Api
from flask_pymongo import PyMongo
from tree.sources import Branch, BranchList, BranchPostList
from auth.sources import Auth

app = Flask("tree_api")
api = Api(app)
mongo = PyMongo(app)


api.add_resource(BranchList, '/branches')
api.add_resource(Branch, '/branch/<uid>')
api.add_resource(BranchPostList, '/branch/<branch_id>/posts')

api.add_resource(Auth, '/auth')
