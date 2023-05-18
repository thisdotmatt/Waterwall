from mongo_db_setup import get_database

dbname = get_database()
collection = dbname["user1_rules"]
def init_db():
    item_1 = {
        "banned_ip" : ["127.222.0.0"],
        "banned_dport" : ["52"],
        "banned_sport" : []
    }
    collection.insert_one(item_1)

def get_db(): #run init before
    item = collection.find()[0]
    return item

collection_length = 0
for item in collection.find():
    collection_length += 1
if collection_length == 0: #collection is empty, initialize
    init_db()

rules = get_db()
banned_ip = rules["banned_ip"]
banned_dport = rules["banned_dport"]
banned_sport = rules["banned_sport"]
