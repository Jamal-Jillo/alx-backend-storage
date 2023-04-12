#!/usr/bin/env python3
""" 9-insert_school.py """


def insert_school(mongo_collection, **kwargs):
    """ inserts a new document in a collection based on kwargs """
    new_school = {}
    for key, value in kwargs.items():
        new_school[key] = value
    result = mongo_collection.insert_one(new_school)
    return result.inserted_id
