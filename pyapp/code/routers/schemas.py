from pydantic import BaseModel, EmailStr
from pydantic.main import Extra

class Login (BaseModel, extra=Extra.forbid):
    username: EmailStr
    password: str

class SignUp (BaseModel, extra=Extra.forbid):
    email: EmailStr
    password: str

class LoginResponse (BaseModel, extra=Extra.forbid):
    status: str
    username: EmailStr
    token: str    

class SignUpResponse (BaseModel, extra=Extra.forbid):
    status: str
    username: EmailStr

class Data (BaseModel, extra=Extra.forbid):
    key: str
    value: str