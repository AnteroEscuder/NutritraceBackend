from pydantic import BaseModel, ConfigDict, EmailStr

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
    model_config = ConfigDict(from_attributes=True)

    id: int
    profile_image_url: str | None = None
