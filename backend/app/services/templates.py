from fastapi.templating import Jinja2Templates

from app.config import settings

templates = Jinja2Templates(directory=settings.templates_dir)
