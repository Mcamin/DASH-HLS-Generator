from pymongo import MongoClient
from dotenv import load_dotenv
import datetime
import os

load_dotenv()
MONGO_URI = os.environ.get("MONGO_URI")
MONGO_DB = os.environ.get("MONGO_DB")


def connect():
    """
    Connect to the mongo database
    Returns: The database instance
    """
    client = MongoClient(MONGO_URI)
    return client[MONGO_DB]


def get_collection(db, collection):
    """
    Get the collection to use for insertion
    Args:
        db: The database to use
        collection: The collection name to retrieve

    Returns: The collection instance

    """
    return db[collection]


def insert_config(collection, config):
    """
    Insert a config in the database
    Args:
        collection: The collection to use
        config: The config to save

    Returns:

    """
    config["last_modified"] = datetime.datetime.utcnow()
    collection.insert_one(config)
    print("Config saved successfully.")


if __name__ == "__main__":
    _db = connect()
    _col = get_collection(_db, "test")
    post = {"author": "Mike",
            "text": "My first blog post!",
            "tags": ["mongodb", "python", "pymongo"]
            }
    insert_config(_col, post)
    
