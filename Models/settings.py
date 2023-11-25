from pymongo import MongoClient
from decouple import config

connnect_string = config("MGDB_CONN_STRING")
client = MongoClient(connnect_string)


class ValidationException(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code
        super().__init__(self.message)


class CustomException(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code
        super().__init__(self.message)
