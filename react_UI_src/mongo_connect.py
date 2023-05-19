from mongo_db_setup import get_database

dbname = get_database()
collection = dbname["user1_rules"]
def init_db(): #creates db if doesn't exist
    collection_length = 0
    for _ in collection.find():
        collection_length += 1
    if collection_length == 0: #collection is empty, initialize
        item_1 = {
            "blocked_ip" : [],
            "blocked_dport" : [],
            "blocked_sport" : [],
            "blocked_proto" : []
        }
        collection.insert_one(item_1)

def get_db(): #run init before
    item = collection.find()[0]
    return item

def update_db(entry, mode, value): #entry = "blocked_ip", etc., mode = "update" or "delete", value = "127.0.0.0" etc. 
    rules = get_db()
    print(rules)
    id = rules["_id"]
    blocked_ip = rules["blocked_ip"]
    blocked_dport = rules["blocked_dport"]
    blocked_sport = rules["blocked_sport"]
    blocked_proto = rules["blocked_proto"]
    #print()
    if entry == "blocked_ip":
        if mode == "update":
            blocked_ip.append(value)
            collection.update_one({"_id": id}, {'$set' : {"blocked_ip" : blocked_ip}})
        elif mode == "delete":
            try:
                blocked_ip.remove(value)
                collection.update_one({"_id": id}, {'$set' : {"blocked_ip" : blocked_ip}})
            except:
                print("Value Not in List")
        else:
            print("Improper Mode\n")
    elif entry == "blocked_dport":
        if mode == "update":
            blocked_dport.append(value)
            collection.update_one({"_id": id}, {'$set' : {"blocked_dport" : blocked_dport}})
        elif mode == "delete":
            try:
                blocked_dport.remove(value)
                collection.update_one({"_id": id}, {'$set' : {"blocked_dport" : blocked_dport}})
            except:
                print("Value Not in List")
        else:
            print("Improper Mode\n")
    elif entry == "blocked_sport":
        if mode == "update":
            blocked_sport.append(value)
            collection.update_one({"_id": id}, {'$set' : {"blocked_sport" : blocked_sport}})
        elif mode == "delete":
            try:
                blocked_sport.remove(value)
                collection.update_one({"_id": id}, {'$set' : {"blocked_sport" : blocked_sport}})
            except:
                print("Value Not in List")
        else:
            print("Improper Mode\n")
    elif entry == "blocked_proto":
        if mode == "update":
            blocked_proto.append(value)
            collection.update_one({"_id": id}, {'$set' : {"blocked_proto" : blocked_proto}})
        elif mode == "delete":
            try:
                blocked_proto.remove(value)
                collection.update_one({"_id": id}, {'$set' : {"blocked_proto" : blocked_proto}})
            except:
                print("Value Not in List")
        else:
            print("Improper Mode\n")
    else:
        print("Entry Not Found\n")
init_db()
update_db("blocked_ip", "update", "8.0.0.0")