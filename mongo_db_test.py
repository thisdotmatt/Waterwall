from mongo_db_setup import get_database

dbname = get_database()
collection = dbname["user1_rules"]
def init_db():
    item_1 = {
        "blocked_ip" : ["127.222.0.0"],
        "blocked_dport" : ["152"],
        "blocked_sport" : ["1234", "130"],
        "blocked_proto" : ["51", "89"]
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
blocked_ip = rules["blocked_ip"]
blocked_dport = rules["blocked_dport"]
blocked_sport = rules["blocked_sport"]
blocked_proto = rules["blocked_proto"]
