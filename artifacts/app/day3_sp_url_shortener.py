import random
import string
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl

app = FastAPI()

url_db = {}

class URLItem(BaseModel):
    url: HttpUrl

def generate_short_code(length: int = 6):
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=length))

@app.post("/shorten")
def shorten_url(url_item: URLItem):
    short_code = generate_short_code()
    while short_code in url_db:
        short_code = generate_short_code()
    
    url_db[short_code] = str(url_item.url)
    return {"short_code": short_code}

@app.get("/{short_code}")
def redirect_to_url(short_code: str):
    original_url = url_db.get(short_code)
    
    if not original_url:
        raise HTTPException(status_code=404, detail="Short URL not found")
        
    return RedirectResponse(url=original_url, status_code=301)