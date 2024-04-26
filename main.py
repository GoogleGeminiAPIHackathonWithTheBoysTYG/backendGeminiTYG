import base64
import json
import time
import logging
import requests
import os
import httpx

from fastapi import FastAPI, UploadFile, BackgroundTasks, Header
from fastapi.responses import FileResponse
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel, Extra
from supabase import create_client, Client

import google.generativeai as genai

app = FastAPI()
logging.basicConfig(level=logging.INFO)

supabaseUrl = 'https://hetpfsivwrylmfhwtnpz.supabase.co'
supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhldHBmc2l2d3J5bG1maHd0bnB6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTMwMjA5MzUsImV4cCI6MjAyODU5NjkzNX0.KOLWeSx8vn70IS9EWB5LgTnlURYaJEDwhx3miwBJvrU'
supabase: Client = create_client(supabaseUrl, supabaseKey)

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

class Report(BaseModel):
    type: str
    transcript: str
    summary: str
    recordingUrl: str

    class Config:
        extra = Extra.ignore

class MessageWrapper(BaseModel):
    message: Report

def analyze_audio(url):
    prompt = "Listen carefully to the following audio file. Provide a brief summary. Explain what the salesperson could have done better and provide real examples. Also analyze their tone  and emotion and what they did poorly"

    GOOGLE_API_KEY='AIzaSyBHTbvoNMQo_jJPPO-ac87C71uVZBNmPd4'
    genai.configure(api_key=GOOGLE_API_KEY)
    
    response = requests.get(url)
    file_path = 'sample.wav'
    
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print("File downloaded successfully.")
    else:
        print("Failed to download the file.")
        return None

    try:
        your_file = genai.upload_file(path=file_path)
        
        model = genai.GenerativeModel('models/gemini-1.5-pro-latest') 
        response = model.generate_content([prompt, your_file])

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            print("Temporary file deleted successfully.")
    
    return response

def insert_recording(report: Report):
    evaluation = analyze_audio(report.recordingUrl)
    try:
        response = supabase.table('recordings').upsert({
            "recording_url": report.recordingUrl,
            "transcript": report.transcript,
            "feedback": evaluation.text,
            "summary": report.summary
        }).execute()        
    except Exception as e:
        print("An error occurred:", e)

@app.post("/report/")
async def receive_report(wrapper: MessageWrapper):


    report = wrapper.message

    # POST HERE OF report 
    if (report.type == "end-of-call-report"):
        insert_recording(report)


    webhook_url = "https://webhook.site/ee2d2fb6-32aa-4609-869a-27890e2edd93"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(webhook_url, json=report.dict())
            response.raise_for_status()
            print("Payload sent to webhook successfully:", response.status_code)
        except:
            print("An error occurred while sending to the webhook:", err)
            return {"error": "Failed to send data to the webhook", "details": str(err),
                    "received_data_to_resend": report.dict()}

    return {"received_data": report.dict()}
   

# app.mount("/", StaticFiles(directory="/app/frontend/dist"), name="static")
