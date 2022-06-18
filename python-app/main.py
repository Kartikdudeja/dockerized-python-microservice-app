from fastapi import FastAPI
import logging

# logging configuration
logging.basicConfig(level=logging.INFO, filename='app.log', format="%(asctime)s: %(levelname)s: [%(process)d:%(processName)s] (%(filename)s-%(module)s.%(funcName)s): %(message)s")

app = FastAPI()

logger = logging.getLogger(__name__)

@app.get("/")
async def root():
    logger.info('Request Received for default Path')
    return {"message": "Application is Running"}
