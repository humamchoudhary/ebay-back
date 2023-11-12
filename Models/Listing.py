from .models import Models, ValidationException
from .helpers import cur_to_list


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
        "required": ["name", "description", "price", "images"],
    }

    def __init__(
        self,
        name,
        description=None,
        images=[],
        verified=False,
        price=0.0,
        search=False,
        id=None,
    ) -> None:
        super().__init__()
        self.name = name
        if search:
            self.query()
        self.name = self.data["name"] if self.data["name"] else name
        self.description = (
            self.data["description"] if self.data["description"] else description
        )
        if id:
            self.id = self.data.get("_id") if self.data.get("_id") else id
        # self.id = self.data["_id"] if self.data["_id"] else id
        self.images = self.data["images"] if self.data["images"] else images
        self.verified = self.data["verified"] if self.data["verified"] else verified
        self.price = self.data["price"] if self.data["price"] else price

        if not search:
            self.getData()
        else:
            self._reInit()

    def query(self):
        if self.name:
            data = cur_to_list(
                self.db.find_one({"name": {"$regex": f"{self.name}", "$options": "i"}}),
                first=True,
            )

            self.data.update(data)
            return self.data
        elif self.id:
            data = cur_to_list(
                self.db.find_one({"_id": {"$regex": f"{self.id}", "$options": "i"}}),
                first=True,
            )

            self.data.update(data)
            return self.data
        else:
            return None
