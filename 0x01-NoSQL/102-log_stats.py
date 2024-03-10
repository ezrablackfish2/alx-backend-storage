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


def get_top_ips(mongo_collection, n=10):
    """
    Returns the top n most present IPs in the collection
    """
    pipeline = [
        {"$group": {
            "_id": {"ip": "$ip"},
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}},
        {"$limit": n}
    ]
    result = mongo_collection.aggregate(pipeline)
    return {doc["_id"]["ip"]: doc["count"] for doc in result}


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx = client.logs.nginx

    print("{} logs".format(get_logs_count(nginx)))
    print("Methods:")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        print("\tmethod {}: {}".
              format(method, get_method_count(nginx, method)))

    print("{} status check".format(get_path_count(nginx,
                                                  "GET", "/status")))

    print("IPs:")
    top_ips = get_top_ips(nginx)
    for ip, count in top_ips.items():
        print("\t{}: {}".format(ip, count))
