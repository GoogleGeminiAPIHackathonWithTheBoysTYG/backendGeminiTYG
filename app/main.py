import base64
import json
import time
import logging

from fastapi import FastAPI, UploadFile, BackgroundTasks, Header
from fastapi.responses import FileResponse
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()
logging.basicConfig(level=logging.INFO)



@app.get("/")
async def root():
    return {"message": "Hello, Blessed World! TYG!"}

# app.mount("/", StaticFiles(directory="/app/frontend/dist"), name="static")
