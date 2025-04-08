from pathlib import Path

from pydantic_settings import BaseSettings

_app_dir = Path(__file__).parent
_project_dir = _app_dir.parent


class Settings(BaseSettings):
    title: str = "FastAPI Backend"
    version: str = "0.1"

    env: str = "development"
    is_prod: bool = env == "production"

    cors_allowed_origins: list[str] = [
        "http://127.0.0.1:3000",
        "http://localhost:3000",
    ]

    project_dir: str = str(_project_dir)
    app_dir: str = str(_app_dir)

    templates_dir: str = str(_app_dir / "routers" / "web" / "templates")

    _static_dir = _app_dir / "static"
    static_dir: str = str(_app_dir / "static")

    logs_folder: str = f"{_app_dir}"
    access_log_file: str = f"{logs_folder}/access.log"
    error_log_file: str = f"{logs_folder}/error.log"
    socketio_log_file: str = f"{logs_folder}/socketio.log"

    access_token_expires: int = 60 * 60  # 1 hour
    refresh_token_expires: int = 60 * 60 * 24  # 24 hours
    web_access_token_expires: int = 60 * 60 * 24 * 7  # 7 days

    SECRET_KEY: str = "yCMLSIKvb8JF29JjxXVRu69pvRvkoAgL1mMJABbJgOQ"
    DATABASE_URI: str = f"sqlite:///{str((_project_dir / 'app.db').resolve())}"

    STRIPE_API_KEY: str = "sk_test_51MqVuLCh3WlIvSBdsFGBsVnm6Z0QtfIuYmm3PhLt8Iy1pIF6UQdwpT3iBJYK2NSl4IGmfXEy72WCqx0j3w8P62WT00AjOmd6wO"
    STRIPE_WEBHOOK_SECRET: str = (
        "whsec_c7ae64dac770c733af0c37aead189504441c5f79db2e2d1e069eaced8bf19a91"
    )

    MAIL_USERNAME: str = "info@theascension.co"
    MAIL_PASSWORD: str = ""

    QUIZ_ID: str = "zWPa15oNvBxkEfulAqRQZOL"

    DOMAIN: str = "http://localhost:8000"


settings = Settings()
