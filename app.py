from pymongo import MongoClient
from flask import Flask, jsonify, session, request, abort
from flask_cors import CORS
from flask_session import Session
from datetime import timedelta, datetime
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from bson.objectid import ObjectId
from decouple import config
from helpers import cur_to_list
from Models import *
import json

app = Flask(__name__)
app.config["SECRET_KEY"] = config("FLASK_SECRET_KEY")


# MongoDB setup
connnect_string = config("MGDB_CONN_STRING")
app.config["MONGO_URI"] = connnect_string
# mongo = PyMongo(app)
# client = mongo.cx
client = MongoClient(connnect_string)


# Session Setup
app.config["SESSION_TYPE"] = "mongodb"
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_MONGODB"] = client
app.permanent_session_lifetime = timedelta(seconds=10)


# Rate Limiter Setup
limiter = Limiter(
    key_func=get_remote_address, app=app, default_limits=["750 per day", "50 per hour"]
)

CORS(app)
sess = Session(app)


def create_response(data=None, message="Success", error=False, status=200):
    """
    Utility function to create a standardized JSON response.
    """
    response = {"status": status, "message": message, "error": error, "data": data}
    return jsonify(response), status


@app.before_request
@limiter.exempt
def sessionCheck():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=15)
    if request.endpoint in ["out"]:
        if session.get("ip") != request.remote_addr:
            abort(401)

            # return jsonify({"message":"unauthorized! Turn of proxy if any active","error":True})


@app.route("/getsessionuser", methods=["POST"])
@limiter.exempt
def sessionUser():
    if session and session.get("user"):
        print(session.items())
        return create_response({"id": session.get("user")})
    else:
        return create_response(error=True, message="No user found", status=401)


@app.route("/user/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    data = json.loads(request.data.decode("utf-8"))
    print(data)
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
        item.valid = True
        item.add()
        return create_response({"id": item.getID()})

    except Exception as e:
        print(e)
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


@app.errorhandler(429)
def toomanyrequests(error):
    return create_response(
        message="too many requests" if not error.description else error.description,
        error=True,
        status=429,
    )


@app.errorhandler(500)
def internalServerError(error):
    print(error.description)
    return create_response(
        message="Internal Server Error" if not error.description else error.description,
        error=True,
        status=500,
    )


@app.errorhandler(404)
def Error404(error):
    print(error.description)
    return create_response(
        message="Page not found" if not error.description else error.description,
        error=True,
        status=404,
    )


@app.errorhandler(401)
def ErrorUnAuth(error):
    return create_response(
        message="Unauthorized" if not error.description else error.description,
        error=True,
        status=401,
    )


@app.errorhandler(403)
def Error(error):
    return create_response(
        message="Error Occured" if not error.description else error.description,
        error=True,
        status=403,
    )


@app.errorhandler(406)
def internalServerError(error):
    return create_response(
        message="Not Acceptable" if not error.description else error.description,
        error=True,
        status=406,
    )


from schedule import every, repeat, run_pending
import threading


@repeat(every(1).hours)
def session_cleanup():
    client.flask_session["sessions"].delete_many(
        {"expiration": {"$lte": datetime.utcnow()}}
    )


import time


def run_schedule():
    while 1:
        run_pending()
        time.sleep(60 * 60)


if __name__ == "__main__":
    # t = threading.Thread(target=run_schedule)
    # t.start()
    app.run(host="0.0.0.0", debug=True)
