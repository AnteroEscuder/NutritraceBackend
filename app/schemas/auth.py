from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginData(BaseModel):
    email: EmailStr
    password: str
