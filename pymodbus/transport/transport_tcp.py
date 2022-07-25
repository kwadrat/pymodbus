"""Transport implementation for TCP."""
import logging
import asyncio

from .transport import Transport

_logger = logging.getLogger()
_logger.setLevel(logging.DEBUG)


class TransportTCP(Transport):
    """Modbus tcp transport layer."""

    def __init__(self, **kwargs):
        """Initialize interface.

        params (specific for tcp, generic parameter documented in Transport):
            host: str, host name or ip address
            port: int, socket port
        """
        print("JAN creating TransportTCP")
        self.host = kwargs.get("host", None)
        self.port = kwargs.get("port", None)
        super().__init__(**kwargs)

    async def start_server_listen(self) -> None:
        """Start server and accept client connections."""
        self.server = await asyncio.start_server(
            self._server_setup_connection_object,
            host=self.host,
            port=self.port,
            reuse_address=True,
            reuse_port=True)

    async def start_client_connect(self) -> None:
        """Start client and connect to server."""
        self.reader, self.writer = await asyncio.open_connection(
            host=self.host,
            port=self.port)
        self.cb_connected(self)

    async def _server_setup_connection_object(self, reader, writer):
        """Loop until disconnect and receive data."""
        conn = TransportTCP(reader=reader, writer=writer)
        self.cb_connected(conn)
