#Replace <MONGO_DB_URI> with your own generated URI, and replace the import statement in mongo_db.py with the name of this file
from pymongo.mongo_client import MongoClient
def get_database():
    uri = "<MONGO_DB_URI>"
    # Create a new client and connect to the server
    client = MongoClient(uri)
    # Send a ping to confirm a successful connection

    return client["rule_db"]

if __name__ == "__main__":
    dbname = get_database()