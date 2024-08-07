from fastapi import FastAPI, Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
import requests
import os

API_KEY = os.getenv("API_KEY")
API_KEY_NAME = "access_token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

app = FastAPI()

def get_api_key(api_key_header: str = Depends(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(status_code=403, detail="Could not validate credentials")

class CountryRequest(BaseModel):
    country: str

@app.post("/get-time")
def get_time(request: CountryRequest, api_key: str = Depends(get_api_key)):
    country = request.country
    response = requests.get(f"https://worldtimeapi.org/api/timezone/{country}")
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=404, detail="Country not found")