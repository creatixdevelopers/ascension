from fastapi.responses import JSONResponse


class AppException(Exception):
    code: int | None = None
    message: str | None = None

    def __init__(self, code: int, message: str | None = None):
        self.code = code
        self.message = message

    def as_json_response(self):
        return JSONResponse(
            content={"status": False, "message": self.message}, status_code=self.code
        )


class BadRequest(AppException):
    def __init__(self, message: str | None = None):
        super().__init__(
            400,
            message if message else "Bad Request",
        )


class Unauthorized(AppException):
    def __init__(self, message: str | None = None):
        super().__init__(
            401,
            message if message else "Unauthorized",
        )


class Forbidden(AppException):
    def __init__(self, message: str | None = None):
        super().__init__(
            403,
            message if message else "Forbidden",
        )


class NotFound(AppException):
    def __init__(self, message: str | None = None):
        super().__init__(
            404,
            message if message else "Not Found",
        )


class MethodNotAllowed(AppException):
    def __init__(self, message: str | None = None):
        super().__init__(
            405,
            message if message else "Method Not Allowed",
        )


class ServerError(AppException):
    def __init__(self, message: str | None = None):
        super().__init__(
            500,
            message
            if message
            else "Server Error - something went wrong, please contact support.",
        )
