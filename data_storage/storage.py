import sys
from pathlib import Path

ABS_PATH = Path(__file__).parent.parent
sys.path.append(str(ABS_PATH))

import pymongo
import threading
from typing import List, Dict
from config import spider_config
from motor import motor_asyncio


# class ClientSingleton(type):
#     __lock = threading.Lock()

#     def __call__(cls, config: spider_config.):
#         if not hasattr(cls, "_instance"):
#             with cls._mutex_instance:
#                 if not hasattr(cls, "_instance"):
#                     cls._instance = super().__call__(config)
#                     try:
#                         conn_str = config.
#             return cls._instance
#         return cls._instance


# class Mongo(metaclass=ClientSingleton):
#     def __init__(self, config=None) -> None:
#         self.config = config or spider_config.LocalStorage()
#         self.client = pymongo.MongoClient(self.config.conn_str)


class AsyncMongo:
    _lock = threading.Lock()
    _instance = dict()

    def __new__(cls, config=None):
        if cls not in cls._instance:
            with cls._lock:
                if cls not in cls._instance:
                    cls._instance[cls] = super().__new__(cls)
                    cls.__init__(cls._instance[cls], config=config)
                    cls._instance[cls].client = motor_asyncio.AsyncIOMotorClient(cls._instance[cls].config.conn_str)
                    db = cls._instance[cls].config.storage_path[0]
                    coll = cls._instance[cls].config.storage_path[1]
                    cls._instance[cls].coll = cls._instance[cls].client[db][coll]
        return cls._instance[cls]

    def __init__(self, config=None) -> None:
        self.config = config or spider_config.LocalStorage()


    # def __init__(self, config=None) -> None:
    #     self.config = config or spider_config.LocalStorage()
    #     self.__client = pymongo.MongoClient(self.config.conn_str)
    #     self.db = self.__client[self.config.storage_path[0]]
    #     self.coll = self.db[self.config.storage_path[1]]

    # def insert_many(self, data: List[Dict], **kwargs):
    #     with self._lock:
    #         self.coll.insert_many(data, **kwargs)
    #     print('Mongodb data insert successfully.')

    # def insert_one(self, record: Dict, **kwargs):
    #     with self._lock:
    #         self.coll.insert_one(record, **kwargs)
    #     print(f'insert successfully:\n{record}\n')


if __name__ == '__main__':
    mongo = Mongo(spider_config.LocalStorage())
    mongo.coll.insert_one({'name': 'John'})