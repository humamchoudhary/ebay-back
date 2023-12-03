from pymongo import MongoClient
from decouple import config
from bson.objectid import ObjectId

connnect_string = config("MGDB_CONN_STRING")
client = MongoClient(connnect_string)
userDB = client["users"]["user"]
adminDB = client["admin"]


def get_username(userid):
    return userDB.find_one({"_id": ObjectId(userid)})["username"]


def get_adminname(adminid, admintype):
    return adminDB[admintype].find_one({"_id": ObjectId(adminid)})["username"]
