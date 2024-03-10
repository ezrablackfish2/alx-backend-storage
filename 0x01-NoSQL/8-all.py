#!/usr/bin/env python3
"""
8-all
"""


def list_all(mongo_collection):
    """
    lists all documents of the collection
    """
    documents = list(mongo_collection.find())
    return documents
