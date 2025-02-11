from pydantic import BaseModel


class UserSchema(BaseModel):
    user_name: str
    password: str
    role: str
    email: str


class PartialUserSchema(BaseModel):
    password: str | None = None
    email: str | None = None
