from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["threateye"]
scans = db["scan_history"]