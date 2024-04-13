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

@app.get("/floorplans/")
async def floorplans():
    return [{'name': '4x4', 'unitsAvailable': '8', 'sqFt': 1302, 'pic': 'https://medialibrarycf.entrata.com/12773/MLv3/4/22/2022/3/26/15165/5dc5e18d44ced1.25555942937.jpg', 'rooms': [{'type': 'Bedroom', 'count': 4}, {'type': 'Bathroom', 'count': 4}], 'description': 'Enjoy our fully-furnished apartments equipped with smart locks, Alexa technology, in-unit laundry, and more!Schedule a tour today!'}, {'name': '5x5 Townhome', 'unitsAvailable': '7', 'sqFt': 1949, 'pic': 'https://medialibrarycf.entrata.com/12773/MLv3/4/22/2022/3/26/15163/5dcae96095f442.47368490621.jpg', 'rooms': [{'type': 'Bedroom', 'count': 5}, {'type': 'Bathroom', 'count': 5}], 'description': 'Spacious 5 private bedroom floor plan. Our largest floor plan option available in our gorgeous townhome layouts. Enjoy fully-furnished apartments equipped with smart locks, Alexa technology, in-unit laundry, and more.Schedule a tour today!'}, {'name': '3x3', 'unitsAvailable': '4', 'sqFt': 1134, 'pic': 'https://medialibrarycf.entrata.com/12773/MLv3/4/22/2022/3/26/15164/5dc5e16684e082.77139189219.jpg', 'rooms': [{'type': 'Bedroom', 'count': 3}, {'type': 'Bathroom', 'count': 3}], 'description': 'Enjoy our fully-furnished apartments equipped with smart locks, Alexa technology, in-unit laundry, and more.Schedule a tour today!'}]



# app.mount("/", StaticFiles(directory="/app/frontend/dist"), name="static")
