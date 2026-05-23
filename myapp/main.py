import time
import random
import structlog
from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator

structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ]
)

logger = structlog.get_logger()

app = FastAPI()

Instrumentator().instrument(app).expose(app)

@app.get("/")
def home():
    logger.info("request", endpoint="/", status=200)
    return {"message": "ok"}

@app.get("/slow")
def slow():
    delay = random.uniform(0.1, 0.5)
    time.sleep(delay)
    logger.info("request", endpoint="/slow", status=200, delay_ms=round(delay * 1000))
    return {"message": "slow response", "delay": delay}

@app.get("/error")
def error():
    if random.random() < 0.5:
        logger.warning("request", endpoint="/error", status=500, error="something went wrong")
        raise HTTPException(status_code=500, detail="something went wrong")
    logger.info("request", endpoint="/error", status=200)
    return {"message": "ok this time"}