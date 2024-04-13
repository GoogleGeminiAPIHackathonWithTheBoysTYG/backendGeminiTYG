import base64
import json
import time
import logging
import requests

from fastapi import FastAPI, UploadFile, BackgroundTasks, Header
from fastapi.responses import FileResponse
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()
logging.basicConfig(level=logging.INFO)



@app.get("/")
async def root():
    return {"message": "Hello, Blessed World! TYG!"}

async def search_for_gmbid(term=''):
    try:
        search_term = f"{term}"
        headers = {
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': 'AIzaSyDTluSYwf0t4sD-KZE5B4UjeGHy0GaNLKw',
            'X-Goog-FieldMask': 'places.displayName,places.id,places.formattedAddress,places.nationalPhoneNumber,places.rating,places.userRatingCount,places.websiteUri',
        }

        json_data = {
            'textQuery': search_term,
        }

        response = requests.post('https://places.googleapis.com/v1/places:searchText', headers=headers, json=json_data)
        return response.json().get('places',[{}])
    except:
        return {}

@app.get("/search_gmbid/")
async def get_places(term: str):
    places = await search_for_gmbid(term)
    return {"places": places}

# app.mount("/", StaticFiles(directory="/app/frontend/dist"), name="static")
