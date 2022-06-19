from fastapi import FastAPI
import logging

from routers import login, data

# fastapi instance
app = FastAPI()

# logging instance
logger = logging.getLogger(__name__)

# logging configuration
logging.basicConfig(level=logging.INFO, filename='app.log', format="%(asctime)s: %(levelname)s: [%(process)d:%(processName)s] (%(filename)s-%(module)s.%(funcName)s): %(message)s")

app.include_router(login.router)
app.include_router(data.router)

# default endpoint
@app.get ("/")
async def root():
    logger.info('Request Received for default Path')
    return {"message": "Application is Running"}
