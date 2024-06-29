import json
from typing import List
from pydantic import BaseModel
from storage import Storage

class JSONStorage(Storage):
    def __init__(self, file_path: str = 'products.json'):
        self.file_path = file_path

    def save(self, products: List[BaseModel]):
        data = [product.dict() for product in products]
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)