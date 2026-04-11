import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from api import router
from exceptions import AppError
from logging_util import get_logger
logger = get_logger()
logger.info("backend start")
app = FastAPI()
app.include_router(router)


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message}},
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
