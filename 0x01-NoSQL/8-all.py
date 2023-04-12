#!/usr/bin/env python3
""" 8-all.py """


def list_all(mongo_collection):
    """lists all documents in a collection"""
    if mongo_collection:
        return mongo_collection.find()
    else:
        return []
