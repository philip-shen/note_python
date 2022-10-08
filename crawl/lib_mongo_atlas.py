from pymongo import MongoClient
import urllib.parse

from logger_setup import *

__all__ = [
    'mongodb_conn',
    'mongodb_insert_many',
    'mongodb_search',
    'mongodb_delete_many',
]

def mongodb_conn(json_data, opt_verbose='OFF'):
    url= json_data["url"]
    username=urllib.parse.quote_plus(json_data["username"])
    password=urllib.parse.quote_plus(json_data["password"])
    conn_url= url.format(username,password)

    if opt_verbose.lower() == 'on':
        msg = '\n conn_url: {}'
        logger.info(msg.format(conn_url))
    
    try:
        client=MongoClient(conn_url, connectTimeoutMS=5000, socketTimeoutMS=5000)
        db=client[json_data["db"]]
        coll=db[json_data["collection"]]
        #db = client.test
        print("connected successfully!!")

        return client, db, coll
    except:
        print("Sorry!connection failed!!")    
''' 
MongoDB insertMany and skip duplicates
https://stackoverflow.com/questions/61480444/mongodb-insertmany-and-skip-duplicates
''' 
def mongodb_insert_many(db, coll, list_collections, ordered= True, opt_verbose='OFF'):
    msg = '\n insert collections: {} to DB'
    logger.info(msg.format(len(list_collections) ))

    if opt_verbose.lower() == 'on':
        msg = '\n list_collections: {}'
        logger.info(msg.format(list_collections))

    coll.insert_many(list_collections, ordered=ordered )

def mongodb_search(db, coll, list_search_dicts, opt_verbose='OFF'):
    list_targets= []
    dict_targets= {}

    if len(list_search_dicts) == 0:
       return list_targets    

    if opt_verbose.lower() == 'on':
        msg = '\n list_search_dicts: {}'
        logger.info(msg.format(list_search_dicts))

    for search_dict in list_search_dicts:
        for key, value in search_dict.items():
            # Query the json dcoument based on equality condition 
            for i in coll.find({key: value}):
                #print(i)
                list_targets.append( {key: value} )
                dict_targets.update({key: value})

    return list_targets, dict_targets
''' 
Python Mongodb - Delete_many()
https://acervolima.com/python-mongodb-delete_many/

import pymongo   
client = pymongo.MongoClient("mongodb://localhost:27017/") 
mydb = client["GFG"] 
col = mydb["Geeks"] 
  
query = {"Name": {"$regex": "^A"}} 
d = col.delete_many(query)   
print(d.deleted_count, " documents deleted !!") 
''' 
''' 
How to use "hint" parameter with pymongo's delete_many()

https://stackoverflow.com/questions/69921904/how-to-use-hint-parameter-with-pymongos-delete-many

hint in DeleteMany is only supported on MongoDB 4.4 and above.

@app.get("/delete/{id}")
async def root(id: int):
    db = get_database()
    our_filter = { 'competitionId': { '$in': [30629, 30630] } }
    our_hint = [('competitionId', 1)]
    c = db['key'].delete_many(filter = our_filter,hint = our_hint)
    return {"message": c.deleted_count}
''' 

def mongodb_delete_many(db, coll, dict_filter= {}, list_hint= [], opt_verbose='OFF'):
    
    if opt_verbose.lower() == 'on':
        msg = '\n dict_filter: {};\n list_hint: {}'
        logger.info(msg.format(dict_filter, list_hint))

    #c = coll.delete_many(filter = dict_filter,hint = list_hint)
    c = coll.delete_many(filter = dict_filter)
    return {"message": c.deleted_count}