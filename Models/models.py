from bson.objectid import ObjectId
from .helpers import cur_to_list
from .settings import client
from datetime import datetime
from bson.objectid import ObjectId


class ValidationException(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code
        super().__init__(self.message)


class CustomException(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code
        super().__init__(self.message)


class Models:
    valid = False
    id = None
    meta = {}

    def __init__(self):
        self.db = client[
            self.__class__.__base__.__name__.lower()
            if not self.meta or not self.meta.get("name")
            else self.meta["name"]
        ][self.__class__.__name__.lower()]

    def validate(self):
        self.valid = True
        if self.meta.get("validate"):
            for i in self.meta.get("validate"):
                if not i[1]((self.__dict__[i[0]])):
                    self.valid = False
                    raise ValidationException(f"{i[0]} is Invalid", 406)

        return self.valid

    def _save(self, data):
        if self.valid:
            self.db.insert(data)
        else:
            raise ValidationException("Validate Model before saving", 403)

    def _update(self, data):
        if self.valid:
            print(
                [
                    {"_id": ObjectId(self.find()[0]["_id"])},
                    {"$set": data},
                ]
            )
            self.db.update_one(
                {"_id": ObjectId(self.find()[0]["_id"])}, {"$set": data}, upsert=True
            )
        else:
            raise ValidationException("Validate Model before updating", 403)

    def _remove(self):
        data = self.find()[0]
        if data.get("_id"):
            self.db.delete_one({"_id": ObjectId(data.get("_id"))})
        else:
            raise CustomException("Not Found", 404)

    def getID(self):
        if self.id:
            return self.id
        else:
            data = self.find()[0]

            return data["_id"]

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
                    else {"$regex": "^{}".format(self.__dict__.get(i) or "")}
                    for i in self.meta["searchParams"]
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
                else {"$regex": "^{}".format(self.__dict__.get(i) or "")}
                for i in self.meta["searchParams"]
                if self.__dict__.get(i)
            }
        )

    def getAll(self):
        return cur_to_list(self.db.find())
