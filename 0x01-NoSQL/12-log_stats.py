#!/usr/bin/env python3
""" 12-log_stats.py """


from pymongo import MongoClient

# connect to the MongoDB instance running on the local machine
client = MongoClient()

# switch to the logs database
db = client.logs

# switch to the nginx collection
collection = db.nginx

# get the number of documents in the collection
num_logs = collection.count_documents({})

print(f"{num_logs} logs")

# get the number of documents with each HTTP method
http_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
for method in http_methods:
    num_docs = collection.count_documents({"method": method})
    print(f"    method {method}: {num_docs}")

# get the number of documents with method=GET and path=/status
num_status_check = collection.count_documents({"method": "GET", "path": "/status"})
print(f"{num_status_check} status check")
