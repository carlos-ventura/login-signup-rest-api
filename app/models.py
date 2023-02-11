from pydantic import BaseModel, EmailStr, validator
class User(BaseModel):
    username: str
    fullname: str
    email: EmailStr
    password: str



class UserInDB(BaseModel):
    username: str
    fullname: str
    email: EmailStr
    hashed_password: str
