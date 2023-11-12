from pymongo import MongoClient
from decouple import config

connnect_string = config("MGDB_CONN_STRING")
client = MongoClient(connnect_string)
