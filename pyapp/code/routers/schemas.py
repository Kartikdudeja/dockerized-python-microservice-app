from pydantic import BaseModel, EmailStr
from pydantic.main import Extra

class Login (BaseModel, extra=Extra.forbid):
    username: EmailStr
    password: str

class SignUp (BaseModel, extra=Extra.forbid):
    email: EmailStr
    password: str

class Token(BaseModel):
    accessToken: str
    tokenType: str
    expiresIn: int

class LoginResponse (BaseModel, extra=Extra.forbid):
    status: str
    username: EmailStr
    token: Token

class SignUpResponse (BaseModel, extra=Extra.forbid):
    status: str
    username: EmailStr
    message: str

class Data (BaseModel, extra=Extra.forbid):
    key: str
    value: str

class DataResponse (BaseModel, extra=Extra.forbid):
    status: str
    message: str

class DataAll (BaseModel):
    key: str
    value: str

    class Config:
        orm_mode = True
        extra=Extra.forbid

class UpdateData (BaseModel, extra=Extra.forbid):
    value: str

class TokenData(BaseModel):
    id: str = None
    email: str = None