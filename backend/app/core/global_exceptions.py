
from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_422_UNPROCESSABLE_ENTITY
from app.core.setup_logging import setup_logging

logger = setup_logging(__name__)


def handle_http_exception(app):
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request : Request, exc: HTTPException):
        logger.warning(f"HTTP异常: {exc}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

def handle_validiation_error(app):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning(f"验证错误: {exc}")
        return JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exc.errors()}
        )
    
def handle_generic_exception(app):
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logger.error(f"通用异常: {exc}")
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(exc)}
        )   
    

def setup_exception_handlers(app):
    handle_http_exception(app)
    handle_validiation_error(app)
    handle_generic_exception(app)