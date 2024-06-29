from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel, Field
from typing import List, Optional
from scraper import Scraper
from json_storage import JSONStorage
from redis_storage import RedisStorage
from console_notification import ConsoleNotification
from email_notification import EmailNotification
import json

app = FastAPI()

# Simple static token authentication
def authenticate(token: str = Header(...)):
    if token != "PaOxeMQPSSVBofR9ARArcnA1CJPvAZVr":
        raise HTTPException(status_code=403, detail="Invalid token")

# Request model
class ScrapeRequest(BaseModel):
    limit: Optional[int] = Field(None, description="Limit the number of pages to scrape")
    proxy: Optional[str] = Field(None, description="Proxy string to use for scraping")
    storage: Optional[str] = Field('json', description="Storage type: 'json' or 'redis'")
    notification: Optional[str] = Field('console', description="Notification type: 'console' or 'email'")

# Scraping endpoint
@app.post("/scrape", dependencies=[Depends(authenticate)])
def scrape_data(scrape_request: ScrapeRequest):
    if scrape_request.storage == 'redis':
        storage = RedisStorage()
    else:
        storage = JSONStorage()

    if scrape_request.notification == 'email':
        notification = EmailNotification(
            smtp_server='smtp.example.com',
            smtp_port=587,
            username='your_email@example.com',
            password='your_password',
            to_email='recipient@example.com'
        )
    else:
        notification = ConsoleNotification()

    scraper = Scraper(limit=scrape_request.limit, storage=storage, notification=notification, proxy=scrape_request.proxy)
    scraped_data = scraper.scrape()
    scraper.save_to_storage(scraped_data)
    scraper.notify(len(scraped_data))
    return {"message": f"Scraped {len(scraped_data)} products"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
