import re
from pydantic import BaseModel, EmailStr, field_validator


def validate_password(value: str) -> str:
    """Функция валидации пароля"""
    if len(value) < 8:
        raise ValueError("Пароль должен содержать минимум 8 символов")
    if not any(char.isdigit() for char in value):
        raise ValueError("Пароль должен содержать хотя бы одну цифру")
    if not any(char.isupper() for char in value):
        raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")
    if not re.search(r"[!@#$%^&*]", value):
        raise ValueError("Пароль должен содержать хотя бы один спецсимвол (!@#$%^&*)")
    return value


class UserSchema(BaseModel):
    user_name: str
    password: str
    role: str
    email: EmailStr

    @field_validator("password")
    @classmethod
    def password_validator(cls, value):
        return validate_password(value)


class PartialUserSchema(BaseModel):
    password: str | None = None
    email: EmailStr | None = None

    @field_validator("password")
    @classmethod
    def password_validator(cls, value):
        return validate_password(value)
