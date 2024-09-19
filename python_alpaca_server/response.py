from typing import Any, Dict, Generic, Optional, TypedDict, TypeVar, Union

import structlog
from pydantic import BaseModel

from .request import CommonRequest

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)

common_responses: Dict[Union[int, str], Dict[str, Any]] = {
    400: {"model": str},
    500: {"model": str},
}


class EndpointParameters(TypedDict):
    responses: Dict[Union[int, str], Dict[str, Any]]
    response_model_exclude_unset: bool
    response_model_exclude_none: bool


common_endpoint_parameters: EndpointParameters = {
    "responses": common_responses,
    "response_model_exclude_unset": True,
    "response_model_exclude_none": True,
}

T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    Value: T
    ClientTransactionID: Optional[int] = None
    ServerTransactionID: Optional[int] = None
    ErrorNumber: Optional[int] = None
    ErrorMessage: Optional[str] = None

    @staticmethod
    def from_request(req: CommonRequest, value: T) -> "Response[T]":
        r = Response(
            Value=value,
            ClientTransactionID=req.ClientTransactionID,
            ServerTransactionID=req.ServerTransactionID,
        )

        return r
