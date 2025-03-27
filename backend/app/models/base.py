from datetime import datetime

from sqlalchemy import select, delete, DateTime
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.orm import mapped_column, Mapped, Session

from app.utils import current_datetime


class _Base(object):
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def __repr__(self):
        identifier = (
            self.id if hasattr(self, "id") else self.uid if hasattr(self, "uid") else ""
        )
        return f"<{self.__class__.__name__} {identifier}>"


Base = declarative_base(cls=_Base)
Base.metadata.naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_`%(constraint_name)s`",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class ModelMixin(object):
    __tablename__: str

    @classmethod
    def create(cls, db: Session, **kwargs):
        """
        Create a new instance of the model and add it to the database.
        """
        result = cls(**kwargs)
        db.add(result)
        return result

    @classmethod
    def get(cls, db: Session, pk):
        if hasattr(cls, "id"):
            result = db.execute(select(cls).filter_by(id=pk))
            return result.scalar()
        raise Exception(f"{cls.__tablename__} has no column named 'id'")

    @classmethod
    def uget(cls, db: Session, uid):
        if hasattr(cls, "uid"):
            result = db.execute(select(cls).filter_by(uid=uid))
            return result.scalar()
        raise Exception(f"{cls.__tablename__} has no column named 'uid'")

    @classmethod
    def get_by(cls, db: Session, first=False, **kwargs):
        query = select(cls).filter_by(**kwargs)
        if hasattr(cls, "id"):
            query = query.order_by(cls.id)
        result = db.execute(query)
        return result.scalar() if first else result.scalars()

    @classmethod
    def get_by_or_create(cls, db: Session, **kwargs):
        query = select(cls).filter_by(**kwargs)
        if hasattr(cls, "id"):
            query = query.order_by(cls.id)
        result = db.execute(query)
        if result:
            return result.scalar()
        else:
            result = cls.create(**kwargs)
            return result

    @classmethod
    def filter(cls, db: Session, filters, first=False):
        query = select(cls).filter(*filters)
        if hasattr(cls, "id"):
            query = query.order_by(cls.id)
        result = db.execute(query)
        return result.scalar() if first else result.scalars()

    @classmethod
    def all(cls, db: Session):
        query = select(cls)
        if hasattr(cls, "id"):
            query = query.order_by(cls.id)
        result = db.execute(query)
        return result.scalars()

    @classmethod
    def first(cls, db: Session):
        query = select(cls)
        if hasattr(cls, "id"):
            query = query.order_by(cls.id)
        result = db.execute(query.limit(1))
        return result.scalar()

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def delete(self, db: Session):
        db.delete(self)

    @classmethod
    def clear(cls, db: Session):
        db.execute(delete(cls))


class CreatedMixin(object):
    created: Mapped[datetime] = mapped_column(DateTime, default=current_datetime)


class LastUpdatedMixin(object):
    last_updated: Mapped[datetime] = mapped_column(
        DateTime, default=current_datetime, onupdate=current_datetime
    )
