import re

from pydantic import BaseModel, EmailStr, validator


class User(BaseModel):
    username: str
    fullname: str
    email: EmailStr
    password: str

    @validator('password')
    def password_validator(cls, password):
        if not re.search(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#\$%^&\*])[a-zA-Z\d!@#\$%^&\*\?]{8,}$",
                password):
            raise ValueError("Password must be at least 8 characters long, "
                             "contain at least one lowercase letter, one uppercase letter, "
                             "one number, and one special character (!, @ ,  # , $, %, ^, &, *)"
                             )
        return password


class UserInDB(BaseModel):
    username: str
    fullname: str
    email: EmailStr
    hashed_password: str
