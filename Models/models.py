from bson.objectid import ObjectId
from .helpers import cur_to_list
from .settings import client


class ValidationException(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code
        super().__init__(self.message)


class Models:
    valid = True
    id = None
    meta = {"required": [], "requiredAny": []}

    def __init__(self):
        self.db = client[
            self.__class__.__base__.__name__.lower()
            if not self.meta or not self.meta.get("name")
            else self.meta["name"]
        ][self.__class__.__name__.lower()]

    def validate(self):
        self.valid = True
        if self.meta.get("required"):
            for i in self.meta.get("required"):
                if self.__dict__[i] == None:
                    self.valid = False
                    raise ValidationException(f"{i} is required", 406)
        if self.meta.get("requiredAny"):
            for i in self.meta.get("requiredAny"):
                if self.__dict__[i] != None:
                    break
            else:
                self.valid = False
                raise ValidationException(f"Data not complete", 406)

    def query(self):
        pass

    def _save(self):
        if self.valid:
            self.db.insert(self.data)
        else:
            raise ValidationException("Validate Model before saving", 403)

    def _remove(self):
        if self.valid:
            self.db.delete_one({"_id": ObjectId(self.id)})

    def getData(self):
        self.data.update(
            {k: v for k, v in self.__dict__.items() if k not in ["db", "_id", "valid"]}
        )

        return self.data

    def _reInit(self):
        for key, value in self.data.items():
            if key not in ["db"]:
                setattr(self, key, value)

    def getAll(self):
        return cur_to_list(self.db.find())
