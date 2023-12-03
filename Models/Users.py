from .models import Models, ValidationException, CustomException
import bcrypt
from .validators import EmailValidator, PasswordValidator


class Users(Models):
    def __init__(
        self,
        email=None,
        username=None,
        password=None,
        role="user",
        id=None,
    ) -> None:
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self._id = id
        self.cart = None
        self._meta = {
            "validate": [
                ("email", EmailValidator()),
                ("password", PasswordValidator()),
            ],
            "searchParams": ["_id", "username", "email"],
        }
        super().__init__()

    def login(self):
        if self._valid:
            data = self.find()
            if len(data) == 1:
                if bcrypt.checkpw(
                    str(self.password).encode("utf-8"),
                    data[0]["password"].encode("utf-8"),
                ):
                    self.id = data[0]["_id"]
                    return data[0]["_id"]
                else:
                    raise ValidationException("Invalid Password", 406)
            else:
                raise ValidationException("Invalid Email", 406)
        else:
            raise ValidationException("Validate model first", 403)

    def signup(self):
        if self._valid:
            if not self.db.find_one({"email": self.email}):
                if not self.db.find_one({"username": self.username}):
                    data = {
                        "username": self.username,
                        "email": self.email,
                        "password": str(
                            bcrypt.hashpw(
                                self.password.encode("utf-8"), bcrypt.gensalt()
                            ).decode()
                        ),
                        "role": self.role,
                    }

                    self._save(data)
                    return True
                else:
                    raise ValidationException("Username already exists", 406)
            else:
                raise ValidationException("Email already exists", 406)

        else:
            raise ValidationException("Validate model first", 403)

    # def query(self):
    #     if self.username:
    #         data = cur_to_list(
    #             self.db.find_one(
    #                 {"username": {"$regex": f"{self.username}", "$options": "i"}}
    #             ),
    #             first=True,
    #         )

    #         return data
    #     elif self.email:
    #         data = cur_to_list(
    #             self.db.find_one(
    #                 {"email": {"$regex": f"{self.email}", "$options": "i"}}
    #             ),
    #             first=True,
    #         )
    #         self.data.update(data)
    #         return self.data
    #     elif self.id:
    #         data = cur_to_list(
    #             self.db.find_one({"_id": {"$regex": f"{self.id}", "$options": "i"}}),
    #             first=True,
    #         )
    #         self.data.update(data)
    #         return self.data
    #     else:
    #         return None


class User(Users):
    def __init__(self, email=None, username=None, password=None, id=None) -> None:
        super().__init__(email, username, password, "user", id)

    def checkout(self):
        if self._valid:
            self.reinit()
            if self.cart:
                amount = 0
                for i in self.cart:
                    amount += i.amount
                return amount
            else:
                CustomException("Empty Cart", code=403)
        else:
            raise CustomException("Validate Model First", code=401)

    def editCart(self, item, quantity):
        self.reinit()
        print(self.cart)
        # l = Listing(id=itemId)
        if item.reinit():
            itemId = item._id
            for i, item in enumerate(self.cart):
                if item["id"] == itemId:
                    self.cart[i]["quantity"] += quantity
                    self.cart[i]["price"] = l.price
                    if self.cart[i]["quantity"] <= 0:
                        self.cart.pop(i)
                    break
            else:
                self.cart.append({"id": itemId, "quantity": quantity, "price": l.price})
                if self.cart[i]["quantity"] <= 0:
                    self.cart.pop()
            self._update({"cart": self.cart})
        else:
            raise CustomException("Product not found", 403)


class Admin(Users):
    def __init__(
        self, email=None, username=None, password=None, role=None, id=None
    ) -> None:
        super().__init__(email, username, password, role, id)


class Moderator(Admin):
    def __init__(self, email=None, username=None, password=None, id=None) -> None:
        super().__init__(email, username, password, "moderator", id)

    def verify(self, item):
        if self.role == "admin":
            item.verified = not item.verified
        else:
            raise CustomException("UnAuthorized", 401)


class SuperUser(Admin):
    def __init__(self, email=None, username=None, password=None, id=None) -> None:
        super().__init__(email, username, password, "superuser", id)


class Developer(Admin):
    def __init__(self, email=None, username=None, password=None, id=None) -> None:
        super().__init__(email, username, password, "developer", id)


class CustomerService(Admin):
    def __init__(self, email=None, username=None, password=None, id=None) -> None:
        super().__init__(email, username, password, "customerservice", id)
