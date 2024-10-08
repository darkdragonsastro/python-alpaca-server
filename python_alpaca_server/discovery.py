import json
from typing import Optional

import asyncudp
import structlog

logger: structlog.stdlib.BoundLogger = structlog.get_logger()


class DiscoveryServer:
    def __init__(self, http_port: int = 80):
        self.socket: Optional[asyncudp.Socket] = None
        self.http_port = http_port

    async def start(self):
        self.socket = await asyncudp.create_socket(local_addr=("0.0.0.0", 32227))

        while True:
            data, addr = await self.socket.recvfrom()

            logger.debug("Received data", data=data, addr=addr)

            if data == b"alpacadiscovery1":
                logger.info("Sending response")
                self.socket.sendto(
                    json.dumps({"AlpacaPort": self.http_port}).encode(), addr
                )
