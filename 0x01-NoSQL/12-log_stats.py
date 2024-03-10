#!/usr/bin/env python3
"""
12-log_stats
"""
from pymongo import MongoClient


def get_logs_count(mongo_collection):
    """
    Returns the number of logs in the collection
    """
    return mongo_collection.count_documents({})


def get_method_count(mongo_collection, method):
    """
    Return method count
    """
    return mongo_collection.count_documents({"method": method})


def get_path_count(mongo_collection, method, path):
    """
    Return number of documents with method and path
    """
    return mongo_collection.count_documents({"method": method, "path": path})


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx = client.logs.nginx

    print("{} logs".format(get_logs_count(nginx)))
    print("Methods:")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        print("\tmethod {}: {}".format(method, get_method_count(nginx, method)))

    print("{} status check".format(get_path_count(nginx,
                                                  "GET", "/status")))
