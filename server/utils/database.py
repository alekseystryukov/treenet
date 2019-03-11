from bson.objectid import ObjectId


class classproperty(object):

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


class QueryModel:
    collection_name = None
    collections = {}

    @classproperty
    def collection(self):
        from app import mongo, app

        name = self.collection_name
        assert name is not None, "You must define 'collection_name'"
        if name not in self.collections:
            with app.app_context():
                actual_name = "TEST_{}".format(name) if app.testing else name
                self.collections[name] = getattr(mongo.db, actual_name)
        return self.collections[name]

    def get_id(self):
        return self._id

    def set_id(self, value):
        self._id = ObjectId(value)

    id = property(get_id, set_id)

    #  query methods
    def save(self):
        if self._id:
            update = self.to_primitive()
            del update["_id"]
            self.collection.update_one(
                {"_id": self._id}, {"$set": update},
            )
        else:
            uid = self.collection.insert(self.to_primitive())
            self._id = uid
        return self

    def to_output(self):
        res = self.to_primitive()
        res["id"] = res["_id"]
        del res["_id"]
        return res

    @classmethod
    def get_list(cls, filters=None):
        filters = filters or {}
        items = cls.collection.find(filters)
        return [cls(i).to_output() for i in items]

    @classmethod
    def get(cls, uid):
        uid = ObjectId(uid)
        res = cls.collection.find_one({"_id": uid})
        return cls(res)

    @classmethod
    def delete(cls, uid):
        uid = ObjectId(uid)
        cls.collection.delete_one({"_id": uid})
