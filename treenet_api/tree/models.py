# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mongoengine import *
from mongoengine.errors import ValidationError


class BranchFeature(EmbeddedDocument):
    name = StringField(required=True, min_length=3, max_length=300)
    representation = StringField(
        required=True, choices=("number", "string", "choices")
    )
    choices_values = ListField(StringField())


class Branch(Document):
    name = StringField(required=True, min_length=3, max_length=300)
    description = StringField()

    features = EmbeddedDocumentListField(BranchFeature)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    parent_id = ObjectIdField()

    # def get_parent(self):
    #     if self.parent_id:
    #         return self.get(self.parent_id)
    #
    # def set_parent(self, value):
    #     self.parent_id = value.id
    #
    # parent = property(get_parent, set_parent)

    @property
    def features_dict(self):
        return {f["name"]: f for f in self.features}


class BranchPost(Document):

    branch_id = StringField(required=True)
    values = DictField()
    text = StringField(max_length=2000)

    @property
    def branch(self):
        try:
            return Branch.objects.get(pk=self.branch_id)
        except Branch.DoesNotExist:
            return
