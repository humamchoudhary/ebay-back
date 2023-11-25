from bson.objectid import ObjectId
from .helpers import cur_to_list
from .settings import client, ValidationException, CustomException
from datetime import datetime
from bson.objectid import ObjectId


class Models:
    def __init__(self):
        self._valid = False
        self._id = None
        # self._meta = {}
        self.db = client[
            self.__class__.__base__.__name__.lower()
            if not self._meta or not self._meta.get("name")
            else self._meta["name"]
        ][self.__class__.__name__.lower()]

    def validate(self):
        self._valid = True
        if self._meta.get("validate"):
            for i in self._meta.get("validate"):
                if not i[1]((self.__dict__[i[0]])):
                    self._valid = False
                    raise ValidationException(f"{i[0]} is Invalid", 406)

        return self._valid

    def _save(self, data):
        if self._valid:
            self.db.insert(data)
        else:
            raise ValidationException("Validate Model before saving", 403)

    def _update(self, data):
        if self._valid:
            self.db.update_one(
                {"_id": ObjectId(self.find()[0]["_id"])}, {"$set": data}, upsert=True
            )
            data = self.db.find_one({"_id": ObjectId(self.find()[0]["_id"])})

        else:
            raise ValidationException("Validate Model before updating", 403)

    def _remove(self):
        data = self.find()[0]
        if data.get("_id"):
            self.db.delete_one({"_id": ObjectId(data.get("_id"))})
        else:
            raise CustomException("Not Found", 404)

    def getID(self):
        if self._id:
            return self._id
        else:
            data = self.find()[0]

            return data["_id"]

    def reinit(self):
        data = self.find()[0]
        if data:
            for k, v in data.items():
                self.__setattr__(k, v)
            return True
        else:
            return False

    def find(self):
        return cur_to_list(
            self.db.find(
                {
                    i: ObjectId(self.__dict__.get(i))
                    if i == "_id"
                    else {"$eq": self.__dict__.get(i)}
                    if isinstance(self.__dict__.get(i), float)
                    or isinstance(self.__dict__.get(i), int)
                    else {"$in": self.__dict__.get(i)}
                    if isinstance(self.__dict__.get(i), list)
                    else {"$eq": self.__dict__.get(i)}
                    if isinstance(self.__dict__.get(i), datetime)
                    else {"$regex": "{}".format(self.__dict__.get(i) or "")}
                    for i in self._meta["searchParams"]
                    if self.__dict__.get(i)
                }
            ),
        )

    def testFind(self):
        return self.db.find(
            {
                i: ObjectId(self.__dict__.get(i))
                if i == "_id"
                else {"$eq": self.__dict__.get(i)}
                if isinstance(self.__dict__.get(i), float)
                or isinstance(self.__dict__.get(i), int)
                else {"$in": self.__dict__.get(i)}
                if isinstance(self.__dict__.get(i), list)
                else {"$eq": self.__dict__.get(i)}
                if isinstance(self.__dict__.get(i), datetime)
                else {"$regex": "{}".format(self.__dict__.get(i) or "")}
                for i in self._meta["searchParams"]
                if self.__dict__.get(i)
            }
        )

    def getAll(self):
        return cur_to_list(self.db.find())
