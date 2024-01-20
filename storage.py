from abc import ABC, abstractmethod
import config
import pymongo
from uuid import uuid4


class BaseStorage(ABC):
    @abstractmethod
    def create(self, advertisement: dict):
        pass

    @abstractmethod
    def get_list(self, skip: int = 0, limit: int = 10, search_param: dict = None):
        pass

    @abstractmethod
    def get_one(self, search_param: dict):
        pass

    @abstractmethod
    def update(self, search_param: dict, obj: dict):
        pass

    @abstractmethod
    def delete(self, search_param: dict):
        pass


class MongoStorage(BaseStorage):
    def __init__(self):
        client = pymongo.MongoClient(config.MONGO_URL)
        db = client[config.MONGO_DATABASE]
        self.collection = db[config.MONGO_TABLE]

    def create(self, advertisement: dict) -> dict:
        advertisement['uuid'] = str(uuid4())
        self.collection.insert_one(advertisement)
        return advertisement

    def get_list(self, skip: int = 0, limit: int = 10, search_string=None):
        if search_string:
            search_regex = {'$regex': f".*{search_string}.*", '$options': 'i'}
            # search_regex_year = {'$regex': search_string}
            a =  type(search_string)
            params = [
                {'model': search_regex},
                {'manufacturer': search_regex},
                {'description': search_regex},
                {'year': int(search_string) if search_string.isdigit() else ''}
            ]
            search_params = {'$or': params}
        else:
            search_params = {}

        return self.collection.find(search_params).skip(skip).limit(limit)

    def get_one(self, search_param: dict):
        return self.collection.find_one(search_param)

    def update(self, search_param: dict, advertisement: dict):
        return self.collection.update_one(search_param, {"$set": advertisement})

    def delete(self, search_param: dict):
        return self.collection.delete_one(search_param)


storage = MongoStorage()
