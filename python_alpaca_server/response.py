import threading
from typing import Generic, Optional, TypeVar

import structlog
from pydantic import BaseModel, Field

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)

common_responses = {400: {"model": str}, 500: {"model": str}}

common_endpoint_parameters = {
    "responses": common_responses,
    "response_model_exclude_unset": True,
    "response_model_exclude_none": True,
}

T = TypeVar("T")


counter_lock = threading.Lock()
counter = 0


def _server_transaction_id() -> int:
    global counter

    with counter_lock:
        counter += 1

    return counter


class CommonRequest(BaseModel):
    ClientTransactionID: Optional[int] = None
    ClientID: Optional[int] = None


class Response(BaseModel, Generic[T]):
    Value: T
    ClientTransactionID: Optional[int] = None
    ServerTransactionID: int = Field(default_factory=_server_transaction_id)
    ErrorNumber: Optional[int] = None
    ErrorMessage: Optional[str] = None

    @staticmethod
    def from_request(req: CommonRequest, value: T) -> "Response[T]":
        r = Response(
            Value=value,
            ClientTransactionID=req.ClientTransactionID,
        )

        logger.info("converting response", r=r)

        return r
