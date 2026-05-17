import time
import random
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
def home():
    return {"message": "ok"}

@app.get("/slow")
def slow():
    delay = random.uniform(0.5, 2.0)
    time.sleep(delay)
    return {"message": "slow response", "delay": delay}

@app.get("/error")
def error():
    if random.random() < 0.5:
        raise HTTPException(status_code=500, detail="something went wrong")
    return {"message": "ok this time"}