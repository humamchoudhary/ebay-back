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
    key_func=get_remote_address, app=app, default_limits=["200 per day", "50 per hour"]
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
    if request.endpoint in ["out"]:
        if session.get("ip") != request.remote_addr:
            # redirect("/",code=401)
            # abort(401)
            pass
            # return jsonify({"message":"unauthorized! Turn of proxy if any active","error":True})


@app.route("/user/login", methods=["POST", "GET"])
@limiter.limit("5 per min")
def login():
    data = json.loads(request.data.decode("utf-8"))
    user = User(email=data.get("email"), password=data.get("password"), search=True)
    # user.validate()
    return create_response(user.login())


@app.route("/out")
@limiter.exempt
def out():
    return create_response(
        cur_to_list(
            client.users["user"].find({"_id": ObjectId("654f9063c5e874f710d93e3b")}),
            first=True,
        )
    )


@app.errorhandler(429)
def toomanyrequests(error):
    return create_response(message="too many requests", error=True, status=429)


@app.errorhandler(500)
def internalServerError(error):
    return create_response(message="Internal Server Error", error=True, status=500)


@app.errorhandler(404)
def internalServerError(error):
    return create_response(message="Page not found", error=True, status=404)


@app.errorhandler(401)
def internalServerError(error):
    return create_response(message="Unauthorized", error=True, status=401)


if __name__ == "__main__":
    client.flask_session["sessions"].delete_many(
        {"expiration": {"$lte": datetime.utcnow()}}
    )
app.run(host="0.0.0.0", debug=True)

# if __name__ == "__main__":
#     u = User("humam", email="humamemail", password="1234123", search=True)
#     print(u.__dict__)
#     print(u.validate())
#     u.signup()
