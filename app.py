from fastapi import Request, Depends, status, Query, FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import random

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
collection = db["advices"]

app = FastAPI()
API_KEY = os.getenv("API_KEY")

def verify_token(request: Request):
    token = request.headers.get("X-API-Key")
    if token != API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")

class Advice(BaseModel):
    category: str
    text: str

@app.get("/evil-advice")
def get_random_advice():
    advices = list(collection.find({}, {"_id": 0}))
    if not advices:
        raise HTTPException(status_code=404, detail="No advice found.")
    return {"evil_advice": random.choice(advices)}

@app.post("/evil-advice")
def add_advice(advice: Advice):
    collection.insert_one(advice.dict())
    return {"message": "Advice added!"}

@app.get("/evil-advices")
def get_all_advices(category: str = None):
    query = {"category": category} if category else {}
    advices = list(collection.find(query, {"_id": 0}))
    return {"advices": advices}

@app.get("/evil-advice/random")
def get_random(category: str = None):
    query = {"category": category} if category else {}
    advices = list(collection.find(query, {"_id": 0}))
    if not advices:
        raise HTTPException(status_code=404, detail="No advice found.")
    return {"evil_advice": random.choice(advices)}

@app.get("/categories")
def get_categories():
    categories = collection.distinct("category")
    return {"categories": categories}