import sys
from pathlib import Path

import typer

current_path = Path(__file__).resolve().parent
sys.path.append(current_path)

from app.models import Base, Permission, Role, User, Quiz
from app.services.db import engine, session

dev = typer.Typer()


@dev.command("create")
def create():
    Base.metadata.create_all(bind=engine)
    print("Database Created!")


@dev.command("clear")
def clear():
    typer.confirm("Are you sure you want to clear the database?", abort=True)
    Base.metadata.drop_all(bind=engine)
    print("Database Cleared!")


@dev.command("add_data")
def add_data():
    db = session()

    admin_dashboard_permission = Permission.create(db=db, name="admin_dashboard.*")
    user_dashboard_permission = Permission.create(db=db, name="user_dashboard.*")
    permissions = {
        "admin_dashboard.*": admin_dashboard_permission,
        "user_dashboard.*": user_dashboard_permission,
    }

    resources = ["permission", "role", "user", "quiz", "response"]
    for resource in resources:
        permissions[f"{resource}.*"] = Permission.create(db=db, name=f"{resource}.*")
        for action in ["create", "read", "update", "delete"]:
            permissions[f"{resource}.{action}"] = Permission.create(
                db=db, name=f"{resource}.{action}"
            )
            permissions[f"{resource}.{action}.all"] = Permission.create(
                db=db, name=f"{resource}.{action}.all"
            )

    admin_role = Role.create(db=db, name="admin")
    admin_role.permissions.extend(
        permissions[permission]
        for permission in ["permission.*", "role.*", "user.*", "quiz.*", "response.*"]
    )

    user_role = Role.create(db=db, name="user")
    user_role.permissions.extend(
        permissions[permission]
        for permission in [
            "user_dashboard.*",
            "quiz.read",
            "response.create",
            "response.read",
            "response.update",
            "response.delete",
        ]
    )

    User.create(
        db=db,
        role=admin_role,
        email="admin@app.com",
        name="Admin",
        phone="1234567890",
        password="password",
        verified=True,
        active=True,
    )

    User.create(
        db=db,
        role=user_role,
        email="user@app.com",
        name="User",
        phone="9876543210",
        password="password",
        verified=True,
        active=True,
    )

    Quiz.create(
        db=db,
        uid="zWPa15oNvBxkEfulAqRQZOL",
        name="Quiz 1",
    )

    db.commit()
    db.close()
    print("Data Added!")


@dev.command("reset")
def reset():
    typer.confirm("Are you sure you want to reset the database?", abort=True)
    clear()
    create()
    add_data()


app = typer.Typer()
app.add_typer(dev, name="dev")

if __name__ == "__main__":
    app()
