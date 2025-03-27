import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from app.routers import api_router, web_router
from app.config import settings
from app.services.exceptions import AppException

logger = logging.getLogger(__name__)
app = FastAPI(
    title=settings.title,
    version=settings.version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(404)
async def custom_404_handler(request: Request, e: AppException) -> JSONResponse:
    ex = AppException(code=404, message="Not Found")
    return ex.as_json_response()


@app.exception_handler(AppException)
async def app_error_handler(request: Request, e: AppException):
    return e.as_json_response()


app.include_router(api_router)
app.include_router(web_router)
app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
