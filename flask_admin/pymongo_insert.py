def get_database():
    from pymongo import MongoClient
    import pymongo

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    Pclient = MongoClient("mongodb+srv://linp:awfWtvUqiS7H401w@pursucluster.2qgve.mongodb.net/PursuDB?retryWrites=true&w=majority")
    
    PursuDB = Pclient['items_list']
    # Create a new collection
    item_list = PursuDB["user_1_items"]

    for item in item_list.find():
        # This does not give a very readable output
        print(item)#'Returning ONE DB object:', item_list.find())
    return item_list.find()
    #return Pclient['items_list']

def update_database():
    from pymongo import MongoClient
    import pymongo
    
    Pclient = MongoClient("mongodb+srv://linp:awfWtvUqiS7H401w@pursucluster.2qgve.mongodb.net/PursuDB?retryWrites=true&w=majority")

    PursuDB = Pclient['items_list']
    '''collection_Pursu = PursuDB["user_1_items"]
    item_1 = {
        "_id": "U1IT00001",
        "item_name": "Box",
        "Adress": "Moon"
    }

    item_2 = {
        "_id": "U1IT00002",
        "item_name": "Glass",
        "Adress": "Middle_of_nowhere"
    }
    collection_Pursu.insert_many([item_1, item_2])'''
    # Create the database
    print(Pclient['items_list'])
    return Pclient['items_list']


# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":
    # Get the database
    PursuDB = get_database()
    # Create a new collection
    '''item_list = PursuDB["user_1_items"]

    for item in item_list.find():
        # This does not give a very readable output
        print(item)
    print('Existing DBs:', Pclient.list_database_names())
    print('Cluster:', Pclient['items_list'])'''
