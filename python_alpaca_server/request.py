import threading
from typing import Optional
from pydantic import BaseModel, Field
import structlog

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)

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
    ServerTransactionID: int = Field(default_factory=_server_transaction_id)


class ActionRequest(CommonRequest):
    Action: str
    Parameters: str


class CommandRequest(CommonRequest):
    Command: str
    Raw: str


class PutConnectedRequest(CommonRequest):
    Connected: bool
