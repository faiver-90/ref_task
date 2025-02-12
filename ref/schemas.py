import re

from pydantic import EmailStr, field_validator, BaseModel

from users.schemas import validate_password


class RegisterByRef(BaseModel):
    ref_code: str
    user_name: str
    password: str
    email: EmailStr

    @field_validator("password")
    @classmethod
    def password_validator(cls, value):
        return validate_password(value)
