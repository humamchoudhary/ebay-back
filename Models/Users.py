# # from flask_mongoengine import MongoEngine
# import mongoengine as me
# from flask_login import UserMixin
# from flask_admin.contrib.mongoengine import ModelView
# # db = MongoEngine(app)
# class User(me.Document,UserMixin):
#     id = me.StringField(max_length=128,db_field='_id',editable=False,primary_key = True)
#     name = me.StringField(max_length=128)
#     email = me.EmailField()
#     password = me.StringField()
#     meta = {"db_alias":"users","strict":False}


# class UserView(ModelView):
#     column_list = ('id', 'name', 'email')  # Customize the columns displayed in the list view
#     def delete_model(self, model):
#         # Custom logic for deletion
#         user_id = model.id
#         # Implement your own deletion logic here, for example:
#         # user = User.objects.get(id=user_id)
#         # user.delete()
#         print(f"Deleting user with ID: {user_id}")

#     def

from .models import Models, ValidationException
from .helpers import cur_to_list
import bcrypt


class Users(Models):
    data = {
        "username": None,
        "password": None,
        "email": None,
        "role": "user",
    }
    meta = {**Models.meta, **{"requiredAny": ["email", "username"]}}

    def __init__(
        self,
        username=None,
        id=None,
        email=None,
        password=None,
        role="user",
        search=False,
    ) -> None:
        super().__init__()
        self.username = username
        self.email = email
        if id:
            self.id = self.data.get("_id") if self.data.get("_id") else id
        if search:
            self.query()
        self.password = password
        self.role = role
        if not search:
            self.getData()
        else:
            self._reInit()

    def login(self):
        if self.valid:
            if self.query():
                if (
                    bcrypt.checkpw(
                        str(self.password).encode("utf-8"),
                        self.data.get("password").encode("utf-8"),
                    )
                    and self.data.get("email") == self.email
                ):
                    return self.data.get("_id")
                else:
                    raise ValidationException("Invalid Password Or Email", 406)
            else:
                raise ValidationException("User does not exist", 406)
        else:
            raise ValidationException("Validate model first", 403)

    def signup(self):
        if self.valid:
            if not self.data.get("_id"):
                if not self.db.find_one({"email": self.email}):
                    if not self.db.find_one({"username": self.username}):
                        self.data["password"] = bcrypt.hashpw(
                            self.data["password"].encode("utf-8"), bcrypt.gensalt()
                        ).decode()
                        self._save()
                        return True
                    else:
                        raise ValidationException("Username already exists", 406)
                else:
                    raise ValidationException("Email already exists", 406)
            else:
                raise ValidationException("User already exists", 406)
        else:
            raise ValidationException("Validate model first", 403)

    def query(self):
        if self.username:
            data = cur_to_list(
                self.db.find_one(
                    {"username": {"$regex": f"{self.username}", "$options": "i"}}
                ),
                first=True,
            )
            self.data.update(data)
            return self.data
        elif self.email:
            data = cur_to_list(
                self.db.find_one(
                    {"email": {"$regex": f"{self.email}", "$options": "i"}}
                ),
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

    def __str__(self):
        return f"{self.id}"


class User(Users):
    def roles(self):
        pass
