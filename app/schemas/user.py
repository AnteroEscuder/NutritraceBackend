from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserProfileUpdate(BaseModel):
    name: str
    email: EmailStr

class UserOut(UserBase):
    id: int
    profile_image_url: str | None = None

    class Config:
        from_attributes = True