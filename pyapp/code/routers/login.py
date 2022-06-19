import logging

from fastapi import APIRouter

from schemas import Login, LoginResponse, SignUp, SignUpResponse

logger = logging.getLogger(__name__)

router = APIRouter (
    prefix= "/apigw/login"
)

@router.post ("/", response_model= LoginResponse)
async def login (body: Login):
    logger.info(f'login request received for username: {body.username}')
    res_status = "success"
    res_token = "somerandomstring"
    return {"status": res_status, "username": body.username, "token": res_token}

@router.post ("/signup", response_model= SignUpResponse)
async def login (body: SignUp):
    logger.info(f'signup request received for username: {body.email}')
    res_status = "success"
    return {"status": res_status, "username": body.email}
