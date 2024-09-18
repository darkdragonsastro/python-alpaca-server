import structlog
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp

from .errors import AlpacaError
from .response import Response


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        logger: structlog.stdlib.BoundLogger,
    ):
        super().__init__(app)
        self.logger = logger

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        self.logger.info(
            "Request",
            method=request.method,
            path=request.url.path,
        )

        # process the request and get the response
        response = await call_next(request)

        return response


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
    ):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        try:
            return await call_next(request)
        except AlpacaError as e:
            response = Response[None](
                Value=None,
                ErrorNumber=e.error_number,
                ErrorMessage=e.error_message,
                ClientTransactionID=e.client_transaction_id,
                ServerTransactionID=e.server_transaction_id,
            )

            return JSONResponse(
                response.model_dump(
                    exclude_defaults=True, exclude_none=True, exclude_unset=True
                ),
                status_code=200,
            )
