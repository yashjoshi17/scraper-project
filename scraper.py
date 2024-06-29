import requests
from bs4 import BeautifulSoup
import json
import os
import time
from typing import List, Dict, Optional
from pydantic import BaseModel, HttpUrl
import redis
from storage import Storage
from notification import Notification


# Data model
class Product(BaseModel):
    product_title: str
    product_price: float
    path_to_image: str


class Scraper:
    def __init__(self, storage: Storage, notification: Notification, limit: Optional[int] = None, proxy: Optional[str] = None):
        self.base_url = "https://dentalstall.com/shop"
        self.storage = storage
        self.notification = notification
        self.limit = limit
        self.proxy = proxy
        self.session = requests.Session()
        if self.proxy:
            self.session.proxies = {'http': self.proxy, 'https': self.proxy}
        # In-memory cache
        self.cache: Dict[str, float] = {}

    def scrape_page(self, page_number: int) -> List[Product]:
        url = f"{self.base_url}/page/{page_number}"
        response = self.session.get(url)

        if response.status_code != 200:
            raise Exception(f"Failed to load page {page_number}")

        soup = BeautifulSoup(response.text, 'html.parser')
        products = []
        # Parsing logic here
        for product_card in soup.select(".product-inner"):
            title_tag = product_card.select_one(".woo-loop-product__title a")
            title = title_tag.text.strip() if title_tag else "N/A"

            price_tag = product_card.select_one(".woocommerce-Price-amount.amount bdi")
            price = float(price_tag.text.replace("₹", "").replace(",", "").strip()) if price_tag else 0.0

            image_tag = product_card.select_one(".mf-product-thumbnail img")
            image_url = image_tag['data-lazy-src'] if image_tag else ""
            image_path = self.download_image(image_url)

            product = Product(
                product_title=title,
                product_price=price,
                path_to_image=image_path
            )
            products.append(product)

        return products

    def download_image(self, url: str) -> str:
        response = self.session.get(url)
        image_name = url.split("/")[-1]
        image_path = f"images/{image_name}"
        with open(image_path, 'wb') as f:
            f.write(response.content)
        return image_path

    def scrape(self) -> List[Product]:
        all_products = []
        page_number = 1
        while True:
            try:
                if self.limit and page_number > self.limit:
                    break
                products = self.scrape_page(page_number)
                all_products.extend(products)
                page_number += 1
            except Exception as e:
                print(f"Error on page {page_number}: {e}")
                time.sleep(5)  # Retry after delay
                continue
        return all_products

    def save_to_storage(self, products: List[Product]):
        updated_products = []
        for product in products:
            # Check cache
            if product.product_title in self.cache:
                if self.cache[product.product_title] == product.product_price:
                    # Skip update if price hasn't changed
                    continue

            # Update cache
            self.cache[product.product_title] = product.product_price
            updated_products.append(product)

        # Save only updated products to storage
        self.storage.save(updated_products)

    def notify(self, count: int):
        self.notification.notify(f"Scraped and updated {count} products")
