from fastapi import FastAPI

from routers import login, data
from database import models
from database.database import engine

# fastapi instance
app = FastAPI()

# logging instance
import logging
logger = logging.getLogger(__name__)

# logging configuration
# logging.basicConfig(level=logging.INFO, filename='app.log', format="%(asctime)s: %(levelname)s: [%(process)d:%(processName)s] (%(filename)s-%(module)s.%(funcName)s): %(message)s")
logging.basicConfig(level=logging.INFO, filename='app.log', format="%(asctime)s: %(levelname)s: (%(filename)s-%(module)s.%(funcName)s): %(message)s")

# ORM Engine to create DB Tables using models.py file
models.Base.metadata.create_all(bind=engine)

# Endpoint Request Router
app.include_router(login.router)
app.include_router(data.router)

# default endpoint
@app.get ("/")
async def root():
    logger.info('Request Received for default Path')
    return {"message": "Application is Running."}