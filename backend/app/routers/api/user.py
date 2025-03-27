from fastapi import APIRouter, Request
from sqlalchemy import select, or_, func

from app.models import User, Role
from app.schemas.data_table import DataTableSchema, DataTableResponseSchema
from app.schemas.user import UserReadSchema, UserCreateSchema, UserUpdateSchema
from app.services.auth import requires
from app.services.db import dbDep
from app.services.exceptions import NotFound

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/", response_model=list[UserReadSchema])
@requires(["user.read.all"])
async def _all(request: Request, db: dbDep):
    users = User.all(db=db)
    return [user for user in users]


@router.get("/{uid}/", response_model=UserReadSchema)
@requires(["user.read.all"])
async def _get(request: Request, uid: str, db: dbDep):
    user = User.uget(db=db, uid=uid)
    if user:
        return user
    raise NotFound()


@router.post("/", response_model=UserReadSchema)
@requires(["user.create.all"])
async def _post(request: Request, data: UserCreateSchema, db: dbDep):
    role = Role.get(db=db, pk=data.role)
    if role:
        user = User.create(
            db=db,
            email=data.email,
            name=data.name,
            password=data.password,
            role=role,
        )
        db.commit()
        return user
    raise NotFound()


@router.patch("/{uid}/", response_model=UserReadSchema)
@requires(["user.update.all"])
async def _patch(request: Request, uid: str, data: UserUpdateSchema, db: dbDep):
    user = User.uget(db=db, uid=uid)
    role = Role.get(db=db, pk=data.role)
    if user and role:
        user.update(name=data.name, password=data.password, role=role)
        db.commit()
        return user
    raise NotFound()


@router.delete("/{uid}/", response_model=str)
@requires(["user.delete.all"])
async def _delete(request: Request, uid: str, db: dbDep):
    user = User.uget(db=db, uid=uid)
    if user:
        user.delete(db=db)
        return uid
    raise NotFound()


@router.post("/data-table/", response_model=DataTableResponseSchema[UserReadSchema])
@requires(["user.read.all"])
async def _datatable(request: Request, data: DataTableSchema, db: dbDep):
    query = select(User)
    total = db.execute(select(func.count()).select_from(query.subquery())).scalar_one()

    if data.search:
        query = query.filter(
            or_(
                User.name.like(f"%{data.search}%"),
                User.email.like(f"%{data.search}%"),
            )
        )

    column_mapper = {
        "name": User.name,
        "email": User.email,
        "verified": User.verified,
        "active": User.active,
        "created": User.created,
    }
    order_by = []
    for order_data in data.order:
        if column := column_mapper.get(order_data["id"]):
            order_by.append(column.desc() if order_data["desc"] else column)
    query = query.order_by(*order_by) if order_by else query.order_by(User.id.desc())

    results: list[User] = (
        db.execute(query.offset(data.skip).limit(data.limit)).scalars().all()
    )

    return DataTableResponseSchema[UserReadSchema](
        data=[result for result in results],
        filtered=len(results),
        total=total,
    )
