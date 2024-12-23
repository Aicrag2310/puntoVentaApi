from fastapi import FastAPI, Depends, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from punto_venta_app.settings import Settings, get_settings
from punto_venta_app.models import AppGenericException, MessageResponse
from punto_venta_app.exceptions import ValidationError


def create_app():
    app = FastAPI()

    # cors middleware
    origins = ['*']
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/api/test/message")
    async def get_test_message():
        return {'message': "Test message"}

    @app.get("/api/version")
    async def get_test_message(config: Settings = Depends(get_settings)):
        return {'version': config.version}   

    from .modules import auth
    from .modules import users
    from .modules import product
    from .modules import categories
    from .modules import sales

    app.include_router(auth.router, tags=['auth'])
    app.include_router(users.router, tags=['user'])
    app.include_router(product.router, tags=['product'])
    app.include_router(categories.router, tags=['categories'])
    app.include_router(sales.router, tags=['sales'])

    @app.exception_handler(AppGenericException)
    async def app_generic_exception_handler(request: Request, exc: AppGenericException):
        return JSONResponse(
            status_code=exc.http_response_status_code,
            content=MessageResponse(code=exc.code, message=exc.message).dict(),
        )


    return app
