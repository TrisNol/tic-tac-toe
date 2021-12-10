import pymongo

class DB:
    def __init__(self) -> None:
        self.client = pymongo.MongoClient("localhost", 27017, username='root', password='password')
        self.db = self.client.tic_tac_toe
        self.records_collection = self.db.records
    
    def write_record(self, record: object) -> None:
        self.records_collection.insert_one(record.__dict__)

    def get_amount_off_documents(self) -> int:
        return self.records_collection.count_documents({})

    def get_player_stats(self) -> object:
        query = {}
        return self.records_collection.find(query)