from schematics.models import Model
from schematics.types import StringType, DateTimeType, BaseType
from schematics.types import ListType
from schematics.types.compound import ModelType
from schematics.validate import DataError
from bson.objectid import ObjectId
from utils.database import QueryModel
import datetime


class MongoUIDType(BaseType):

    def to_primitive(self, value, context):
        return str(value)

    def to_native(self, value, context):
        return ObjectId(value)


class BaseModel(QueryModel, Model):

    def __init__(self, *args, **kwargs):
        Model.__init__(self, *args, **kwargs)
        self._object_cache = {}

    def get_from_object_cache(self, class_, uid):
        key = "{}__{}".format(class_.__class__, uid)
        return self._object_cache[key]

    def set_to_object_cache(self, class_, uid, value):
        key = "{}__{}".format(class_.__class__, uid)
        self._object_cache[key] = value


class BranchFeature(Model):
    name = StringType(required=True, min_length=3, max_length=300)
    representation = StringType(
        required=True, choices=("number", "string", "choices")
    )
    choices_values = ListType(StringType)

    def __repr__(self):
        return str(self.to_primitive())


class Branch(BaseModel):
    collection_name = "branches"

    _id = MongoUIDType(serialize_when_none=False)
    name = StringType(required=True, min_length=3, max_length=300)
    description = StringType(max_length=1000)
    features = ListType(ModelType(BranchFeature))

    created_at = DateTimeType(default=datetime.datetime.now)
    parent_id = MongoUIDType()

    def get_parent(self):
        if self.parent_id:
            return self.get(self.parent_id)

    def set_parent(self, value):
        self.parent_id = value.id

    parent = property(get_parent, set_parent)

    def __init__(self, raw_data, *args, **kwargs):
        raw_data["features"] = raw_data.get("features") or []
        super(Branch, self).__init__(raw_data, *args, **kwargs)


class BranchPostValuesType(BaseType):
    pass


class BranchPost(BaseModel):
    collection_name = "branch_posts"

    _id = MongoUIDType(serialize_when_none=False)
    branch_id = MongoUIDType(required=True)
    values = BranchPostValuesType()
    text = StringType(max_length=1000)

    @property
    def branch(self):
        try:
            branch = self.get_from_object_cache(Branch, self.branch_id)
        except KeyError:
            branch = Branch.get(self.branch_id)
            self.set_to_object_cache(Branch, self.branch_id, branch)
        return branch

    @branch.setter
    def set_branch(self, branch):
        self.branch_id = branch.id

    def validate_values(self, data, values):
        features = self.branch.features or []
        features_by_name = {f["name"]: f for f in features}
        if not isinstance(values, dict):
            raise DataError({
                "values": "Values is supposed to be an object(map),"
                          "not the {}".format(type(values))
            })
        for name, value in values.items():
            if name not in features_by_name:
                raise DataError({
                    "name": "The branch doesn't contain such a feature:"
                            " {}".format(name)
                })
            feature_info = features_by_name[name]
            representation = feature_info["representation"]
            if representation == "number":
                try:
                    value = float(value)
                except ValueError:
                    raise DataError(
                        {"value": "'{}' is a wrong number".format(value)})
                else:
                    return value
            elif representation == "string":
                return str(value)
            elif representation == "choices":
                value = str(value)
                if value in feature_info["choices"]:
                    return value
                else:
                    raise DataError(
                        {"value": "'{}' is a wrong choise".format(value)})
