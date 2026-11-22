from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

ERROR_CODES = {
    401: "UNAUTHORIZED",
    403: "FORBIDDEN",
    404: "NOT_FOUND",
    405: "METHOD_NOT_ALLOWED",
    409: "CONFLICT",
}

DEFAULT_MESSAGES = {
    404: "The requested resource was not found.",
    405: "This HTTP method is not supported for this endpoint.",
}


class ApiError(Exception):
    def __init__(self, status_code: int, code: str, message: str, details=None):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details


def success(message: str, data=None, meta=None) -> dict:
    body = {"success": True, "message": message, "data": data}
    if meta is not None:
        body["meta"] = meta
    return body


def error_body(code: str, message: str, details=None) -> dict:
    error = {"code": code, "message": message}
    if details:
        error["details"] = details
    return {"success": False, "error": error}


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(ApiError)
    async def api_error_handler(request: Request, exc: ApiError):
        return JSONResponse(
            status_code=exc.status_code,
            content=error_body(exc.code, exc.message, exc.details),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, exc: RequestValidationError):
        details = []
        for err in exc.errors():
            parts = [str(p) for p in err["loc"] if p not in ("body", "query", "path")]
            details.append({"field": ".".join(parts) or "body", "message": err["msg"]})
        return JSONResponse(
            status_code=400,
            content=error_body(
                "VALIDATION_ERROR",
                "The request contains invalid or missing fields.",
                details,
            ),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_handler(request: Request, exc: StarletteHTTPException):
        code = ERROR_CODES.get(exc.status_code, "ERROR")
        message = DEFAULT_MESSAGES.get(exc.status_code, "Request failed.")
        return JSONResponse(
            status_code=exc.status_code, content=error_body(code, message)
        )

    @app.exception_handler(Exception)
    async def unexpected_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content=error_body("INTERNAL_ERROR", "An unexpected error occurred."),
        )
