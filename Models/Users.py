from .models import Models, ValidationException
import bcrypt
from .validators import EmailValidator, PasswordValidator


class Users(Models):
    meta = {
        "validate": [("email", EmailValidator()), ("password", PasswordValidator())],
        "searchParams": ["_id", "username", "email"],
    }

    def __init__(
        self,
        email=None,
        username=None,
        password=None,
        role="user",
        id=None,
    ) -> None:
        super().__init__()
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self._id = id

    def login(self):
        if self.valid:
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
        if self.valid:
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


class Admin(Users):
    def __init__(self, email=None, username=None, password=None, id=None) -> None:
        super().__init__(email, username, password, "admin", id)
