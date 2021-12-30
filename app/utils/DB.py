import pymongo

class DB:
    def __init__(self) -> None:
        self.client = pymongo.MongoClient(
            "localhost", 27017, username='root', password='password')
        self.db = self.client.tic_tac_toe
        self.records_collection = self.db.records

    def write_record(self, record: object) -> None:
        """Writes record object to the database"""
        self.records_collection.insert_one(record.__dict__)

    def get_entries(self):
        """Returns all played games"""
        return list(self.records_collection.find())

    def get_amount_off_documents(self) -> int:
        """Returns amount of existing games played"""
        return self.records_collection.count_documents({})

    def get_player_stats(self) -> object:
        """Returns player stats"""
        query = {}
        return self.records_collection.find(query)

    def close(self) -> None:
        """Closes the connection to the database"""
        self.client.close()

    def __del__(self):
        self.close()
