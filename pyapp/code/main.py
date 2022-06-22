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

# database connected logic

# @app.on_event("startup")
# async def startup():
#     if not database.is_connected:
#         await database.connect()
#     # create a dummy entry
#     await User.objects.get_or_create(email="test@test.com")


# @app.on_event("shutdown")
# async def shutdown():
#     if database.is_connected:
#         await database.disconnect()