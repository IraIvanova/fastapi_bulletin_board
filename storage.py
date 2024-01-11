from abc import ABC, abstractmethod
import config
import pymongo
from uuid import uuid4


class BaseStorage(ABC):
    @abstractmethod
    def create(self, advertisement: dict):
        pass

    @abstractmethod
    def index(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
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

    def index(self):
        return self.collection.find({})

    def update(self):
        raise NotImplemented

    def delete(self):
        raise NotImplemented


storage = MongoStorage()
