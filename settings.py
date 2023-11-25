from decouple import config
from flask import Flask, jsonify, session, request, abort
from flask_cors import CORS
from flask_session import Session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pymongo import MongoClient, cursor
from datetime import timedelta

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
    response = {"status": status, "message": message, "error": error, "data": data}
    return jsonify(response), status


@app.before_request
@limiter.exempt
def sessionCheck():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=15)
    print(session.items())
    if session and session.get("ip") and session.get("ip") != request.remote_addr:
        abort(401)
    elif not session or not session.get("ip"):
        session["ip"] = request.remote_addr

        # return jsonify({"message":"unauthorized! Turn of proxy if any active","error":True})


@app.route("/getsessionuser", methods=["POST"])
@limiter.exempt
def sessionUser():
    if session and session.get("user"):
        print(session.items())
        return create_response({"id": session.get("user")})
    else:
        return create_response(error=True, message="No user found", status=401)


def cur_to_list(cur, first=False):
    if type(cur) == cursor:
        if not first:
            return [dict(item, _id=str(item["_id"])) for item in cur]
        else:
            return [dict(item, _id=str(item["_id"])) for item in cur][0]
    else:
        cur["_id"] = str(cur["_id"])
        return cur
