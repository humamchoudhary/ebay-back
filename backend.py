from settings import app, limiter, create_response
from Models import User, Listing
from flask import session, request, abort
import json
from datetime import datetime


@app.route("/user/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    data = json.loads(request.data.decode("utf-8"))
    user = User(email=data.get("email"), password=data.get("password"))

    try:
        user.validate()
    except Exception as e:
        abort(e.code, {"message": e.message})
    id = user.login()
    session["user"] = id
    session["ip"] = request.remote_addr
    return create_response({"id": id})


@app.route("/user/signup", methods=["POST"])
@limiter.limit("5 per minute")
def signup():
    data = json.loads(request.data.decode("utf-8"))
    user = User(data.get("email"), data.get("username"), data.get("password"))

    try:
        user.validate()
    except Exception as e:
        abort(e.code, {"message": e.message})
    if user.signup():
        id = user.login()
        session["user"] = id
        session["ip"] = request.remote_addr
        return create_response({"id": id})
    else:
        abort(500)


@app.route("/user/additem", methods=["POST"])
@limiter.limit("20 per day")
def addItem():
    """
    Adds item from database\n
    Takes input from request.data in json form\n
    Params:\n
    \tname : str 'Name of Item'
    \tdescription : str 'Description of Item'
    \timages : list[str] 'List of images of Item'
    \tprice : int 'Price of Item'
    \tcategories : list[str] 'List of categories of items'
    Return:\n
    \t-> response : success | error\n
    \t{\n
    \t"status": item.id if success else None,\n
    \t"message": message,\n
    \t"error": error,\n
    \t"data": item.id if success else None\n
    \t}
    """
    data = json.loads(request.data.decode("utf-8"))
    item = Listing(
        data.get("name"),
        data.get("desc"),
        data.get("images"),
        data.get("price"),
        session.get("user"),
        data.get("categories"),
        creationTime=datetime.now(),
    )

    try:
        item._valid = True
        item.add()
        return create_response({"id": item.getID()})

    except Exception as e:
        abort(e.code, {"message": e.message})


@app.route("/user/searchitem", methods=["GET"])
@limiter.limit("10 per minute")
def searchItem():
    """
    Searches item from database\n
    Takes input from request.data in json form\n
    Params:\n
    \tname : str 'Name of Item'
    \tprice : int 'Price of Item'
    \tcategories : list[str] 'List of categories of items'
    Return:\n
    \t-> response : success | error\n
    \t{\n
    \t"message": message,\n
    \t"status": 200 if success else error codes,\n
    \t"error": error,\n
    \t"data": [items] if success else None\n
    \t}
    """
    data = json.loads(request.data.decode("utf-8"))
    item = Listing(
        name=data.get("name"),
        price=data.get("price"),
        createdBy=session.get("user"),
        categories=data.get("categories"),
        creationTime=None,
        id=data.get("id"),
    )
    try:
        return create_response(item.find())

    except Exception as e:
        abort(e.code, {"message": e.message})


@app.route("/user/delitem", methods=["POST"])
def deleteItem():
    """
    Delete item from database\n
    Takes input from request.data in json form\n
    Params:\n
    \titemId : str 'item id of Item'
    \tuserId : str 'user id of Item'
    Return:\n
    \t-> response : success | error\n
    \t{\n
    \t"message": [items] if success else None,\n
    \t"status": 200 if success else error codes,\n
    \t"error": error,\n
    \t"data": None\n
    \t}
    """
    data = json.loads(request.data.decode("utf-8"))
    item = Listing(id=data.get("itemId"))
    user = User(id=data.get("userId"))
    try:
        item.delete(user)
        return create_response()
    except Exception as e:
        abort(e.code, {"message": e.message})


@app.route("/item/bid", methods=["POST"])
def bidAdd():
    data = json.loads(request.data.decode("utf-8"))
    item = Listing(id=data.get("itemId"))
    user = User(id=data.get("userId"))
    try:
        item.bid(user)
        return create_response()
    except Exception as e:
        abort(e.code, {"message": e.message})


from werkzeug.security import generate_password_hash, check_password_hash


@app.template_filter("hash")
def hash_pass(password):
    return generate_password_hash(password)


def chat(user):
    pass
