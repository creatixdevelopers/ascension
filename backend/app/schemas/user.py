from datetime import datetime

from pydantic import constr, conint, Field

from app.schemas import Model, Email, Password


class UserCreateSchema(Model):
    email: Email
    name: constr(strip_whitespace=True, max_length=128)
    phone: constr(strip_whitespace=True, max_length=16)
    password: Password
    active: bool
    role: conint(ge=1) | None = None


class UserUpdateSchema(Model):
    name: constr(strip_whitespace=True, max_length=132) | None
    phone: constr(strip_whitespace=True, max_length=16) | None
    password: Password | None
    active: bool | None
    role: conint(ge=1)


class UserReadSchema(Model):
    uid: str
    created: datetime
    last_updated: datetime
    email: Email
    name: constr(strip_whitespace=True, max_length=132)
    phone: constr(strip_whitespace=True, max_length=16)
    verified: bool
    active: bool
    role: str = Field(validation_alias="role_name")
    permissions: list[str] = Field(validation_alias="scopes")
