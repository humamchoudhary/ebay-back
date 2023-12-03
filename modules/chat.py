from pymongo import MongoClient
from decouple import config
from bson.objectid import ObjectId
from datetime import datetime
from Models.settings import CustomException

connnect_string = config("MGDB_CONN_STRING")
client = MongoClient(connnect_string)
chatDB = client["users"]["chat"]
userDB = client["users"]["user"]


def createChat(userid, subject, priority):
    inserted = chatDB.insert_one(
        {
            "userId": userid,
            "priority": priority,
            "status": "pending",
            "subject": subject,
            "chat": [],
        }
    )
    userDB.update_one(
        {"_id": ObjectId(userid)}, {"$push": {"chat": inserted.inserted_id}}
    )
    return str(inserted.inserted_id)


def getUserChats(userid):
    chat_ids = userDB.find_one({"_id": ObjectId(userid)})["chat"]
    chats = []
    for id in chat_ids:
        chats.append(getChat(id))
    return chats


def getChat(chatid, current_user):
    chat = chatDB.find_one({"_id": ObjectId(chatid)})
    if chat["userID"] == current_user:
        return chat
    else:
        raise CustomException("Unauthorized", 401)


def sendchatUser(userid, message, chatID):
    chatDB.update_one(
        {"_id": ObjectId(chatID), "userID": userid},
        {
            "$push": {
                "chat": {
                    "sender": userid,
                    "message": message,
                    "timesent": datetime.now(),
                }
            }
        },
    )


def sendchatAdmin(adminid, message, chatID):
    chatDB.update_one(
        {"_id": ObjectId(chatID)},
        {
            "$set": {"status": "active"},
            "$push": {
                "chat": {
                    "sender": adminid,
                    "message": message,
                    "timesent": datetime.now(),
                }
            },
        },
    )
