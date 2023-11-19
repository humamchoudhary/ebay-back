from .models import Models, ValidationException, CustomException
from .helpers import cur_to_list
from datetime import datetime
from .Users import Admin


class Listing(Models):
    data = {
        "name": None,
        "description": None,
        "images": [],
        "verified": False,
        "price": 0,
    }
    meta = {
        **Models.meta,
        "name": "listings",
        "validate": [
            ("name", lambda: True),
            ("createdBy", lambda: True),
            ("categories", lambda: True),
        ],
        "searchParams": [
            "_id",
            "name",
            "price",
            "verified",
            "creationTime",
            "categories",
        ],
        # "required": ["name", "description", "price", "images"],
    }

    def __init__(
        self,
        name=None,
        description=None,
        images=[],
        price=0.0,
        createdBy=None,
        categories=[],
        id=None,
        creationTime=None,
        verified=False,
    ) -> None:
        super().__init__()
        self.name = name
        self.description = description
        self.images = images
        self.verified = verified
        self.price = price
        self.categories = categories
        self.createdBy = createdBy
        self.creationTime = creationTime
        if id:
            self._id = id

    def verify(self, userid):
        if Admin(userid).find() != None:
            if self._id:
                self.verified = True

                self._update(
                    {
                        **self.find()[0],
                        **{
                            "verified": self.verified,
                        },
                    }
                )
            else:
                raise CustomException("please provide an item ID", 401)
        else:
            raise CustomException("UnAuthorized", 401)

    def delete(self, user):
        data = self.find()
        if data:
            if (
                user.valid
                and isinstance(user, Admin)
                or data[0].get("createdBy") == user._id
            ):
                self._remove()
                
            else:
                raise CustomException("UnAuthorized", 401)
        else:
            raise CustomException("Not Found", 404)

    def edit(self, updatedata, user):
        data = self.find()
        print(data)
        if data != None and data[0] != None:
            if user._id == data[0]["createdBy"]:
                if self._id:
                    self._update(updatedata)
                else:
                    raise CustomException("Please provide an item ID", 401)
            else:
                raise CustomException("UnAuthorized", 401)
        else:
            raise CustomException("Item not found", 404)

    def add(self):
        self._save(
            {
                "name": self.name,
                "description": self.description,
                "images": self.images,
                "verified": self.verified,
                "price": self.price,
                "categories": self.categories,
                "createdBy": self.createdBy,
                "creationTime": self.creationTime,
            }
        )
