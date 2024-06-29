# redis_storage.py
import redis
from typing import List
from pydantic import BaseModel
from storage import Storage

class RedisStorage(Storage):
    def __init__(self):
        self.client = redis.Redis(host='localhost', port=6379, db=0)

    def save(self, products: List[BaseModel]):
        for product in products:
            self.client.set(product.product_title, product.json())