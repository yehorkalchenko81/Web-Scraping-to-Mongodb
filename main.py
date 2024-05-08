from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pprint import pprint

client = MongoClient(
    'mongodb+srv://egorkalcenko69:ipadmini@yehorkalchenko.qdnz4xh.mongodb.net/?retryWrites=true&w=majority',
    server_api=ServerApi('1')
)

db = client.database


def decorator(func):
    def inner(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(e)

    return inner


def read_all():
    result = db.cats.find({})
    for i in result:
        pprint(i)


def read_one(name: str):
    result = db.cats.find_one({'name': name})
    pprint(result)


@decorator
def update_age(name: str, age: int):
    db.cats.update_one({'name': name}, {'$set': {'age': age}})


@decorator
def add_feature(name: str, feature: str):
    features = db.cats.find_one({'name': name}, {'features': 1})['features']
    features.append(feature)
    db.cats.update_one({'name': name}, {'$set': {'features': features}})


@decorator
def delete_one(name: str):
    db.cats.delete_one({'name': name})


def delete_all():
    db.cats.delete_many({})


if __name__ == "__main__":
    pass  # Call functions which you want to ckeck
