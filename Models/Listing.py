from .models import Models, ValidationException, CustomException
from .helpers import cur_to_list
from datetime import datetime
from .Users import Admin
from datetime import timedelta


class Listing(Models):
    def __init__(
        self,
        name=None,
        description=None,
        images=[],
        price=0,
        createdBy=None,
        categories=[],
        id=None,
        creationTime=None,
        verified=None,
        isAuction=True,
        endTime=timedelta(days=15),
        startPrice=0.0,
        increaments=0.05,
        discount=0.0,
    ) -> None:
        self.name = name
        self.description = description
        self.images = images
        self.verified = verified
        self.price = price
        self.categories = categories
        self.createdBy = createdBy
        self.creationTime = creationTime

        self.isAuction = isAuction
        self.startPrice = startPrice
        if creationTime:
            self.endTime = creationTime + endTime
        self.increaments = price * increaments
        self.lastbider = None
        self.noOfbids = 0
        self.currentBid = startPrice
        self.discount = discount

        if id:
            self._id = id

        self._meta = {
            "name": "listings",
            "validate": [
                ("name", lambda x: True),
                ("createdBy", lambda x: True),
                ("categories", lambda x: True),
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
        super().__init__()

    def bid(self, user, amount=None):
        self.reinit()
        if self.isAuction:
            if self.lastbider == user._id:
                raise CustomException("Already highest bidder", 401)
            else:
                if amount > self.currentBid + self.increaments:
                    self.currentBid += amount or self.increaments
                    self.lastbider = user._id
                else:
                    raise CustomException("Amount below existing bid", 401)
            self.validate()
            self._update({"lastbider": self.lastbider, "currentBid": self.currentBid})
        else:
            raise CustomException("Cannot Bid", 401)

    def verify(self, userid):
        if Admin(userid).find() != None:
            if self._id:
                self._update(
                    {
                        "verified": not self.find()[0]["verified"],
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
                user._valid
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
                "isAuction": self.isAuction,
                "endTime": self.endTime,
                "startPrice": self.startPrice,
                "increaments": self.increaments,
            }
        )
