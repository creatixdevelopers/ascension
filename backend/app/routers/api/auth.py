from datetime import timedelta

from fastapi import APIRouter, Request, Response

from app.config import settings
from app.models import Role, User
from app.schemas.auth import (
    ForgotPasswordSchema,
    LoginSchema,
    ResetPasswordSchema,
    TokenSchema,
)
from app.schemas.user import UserCreateSchema, UserReadSchema
from app.services.auth import requires
from app.services.db import dbDep
from app.services.exceptions import BadRequest, Forbidden, NotFound, Unauthorized
from app.utils.auth import (
    create_access_token,
    create_jwt,
    create_refresh_token,
    verify_jwt,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login/", response_model=TokenSchema)
async def login(data: LoginSchema, db: dbDep, response: Response):
    user: User = User.get_by(db=db, first=True, email=data.email)
    if user and user.verify_password(data.password):
        if not user.active:
            raise Forbidden(message="Account deactivated, please contact support")

        access_token = create_access_token(user=user, fresh=True)
        refresh_token = create_refresh_token(user=user)
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            samesite="strict",
            max_age=settings.refresh_token_expires + 60,
            secure=settings.is_prod,
        )

        return {"token": access_token, "token_type": "bearer"}
    raise Unauthorized(message="Invalid credentials")


@router.post("/signup/", response_model=TokenSchema)
async def signup(data: UserCreateSchema, db: dbDep):
    role = Role.get_by(db=db, name="user")
    if role:
        user = User.create(
            db=db,
            email=data.email,
            name=data.name,
            phone=data.phone,
            password=data.password,
            verifies=True,
            active=True,
            role=role,
        )
        db.commit()
        return {"status": True, "message": "Successfully created account"}
    raise NotFound()


@router.post("/refresh/", response_model=TokenSchema)
async def refresh(request: Request, db: dbDep, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise Unauthorized(message="Refresh token missing")
    claims = verify_jwt(token=refresh_token)
    uid = claims.get("sub")
    user = User.uget(db=db, uid=uid)

    if user:
        if not user.active:
            raise Forbidden(message="Account deactivated, please contact support")

        access_token = create_access_token(user=user, fresh=False)
        # TODO: Implement refresh token rotation

        return {"token": access_token, "token_type": "bearer"}

    raise Unauthorized(message="Invalid token")


@router.get("/me/", response_model=UserReadSchema)
@requires([])
async def me(request: Request, db: dbDep):
    uid = getattr(request.state, "sub", None)
    scopes = getattr(request.state, "scopes", None)
    if not uid or not scopes:
        raise Unauthorized(message="Invalid token")

    user = User.uget(db=db, uid=uid)
    return user


@router.post("/logout/")
async def logout(request: Request, response: Response):
    response.delete_cookie(key="refresh_token")
    return


@router.post("/forgot-password/")
async def forgot_password(request: Request, data: ForgotPasswordSchema, db: dbDep):
    user = User.get_by(db=db, first=True, email=data.email)
    if not user:
        raise BadRequest(message="Email not registered")
    token = create_jwt({"sub": user.uid}, timedelta(minutes=15))
    # TODO: insert correct email and send email
    reset_link = f"/?token={token}"

    return {"status": True, "message": "Password reset link sent to email"}


@router.post("/reset-password/")
async def reset_password(request: Request, data: ResetPasswordSchema, db: dbDep):
    try:
        payload = verify_jwt(data.token)
        user_uid = payload.get("sub")
        if user := User.uget(db=db, uid=user_uid):
            user.update(password=data.password)
            db.commit()
            return {"status": True, "message": "Password updated successfully"}
        raise BadRequest(message="Invalid or expired token")
    except Exception:
        raise BadRequest(message="Invalid or expired token")
