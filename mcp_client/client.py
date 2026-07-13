import asyncio
import threading
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

MCP_SERVER = str(Path(__file__).resolve().parent.parent / ".venv" / "Scripts" / "wikipedia-mcp.exe")


class WikipediaMCPClient:
    """Persistent MCP client — one subprocess, reused across all calls."""

    def __init__(self):
        self._server = StdioServerParameters(command=MCP_SERVER, args=[])
        self._loop: asyncio.AbstractEventLoop | None = None
        self._session: ClientSession | None = None
        self._thread: threading.Thread | None = None
        self._ready = threading.Event()

    def start(self):
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        self._ready.wait()

    def _run_loop(self):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._connect())
        self._loop.run_forever()

    async def _connect(self):
        self._cm = stdio_client(self._server, errlog=open("nul", "w"))
        read, write = await self._cm.__aenter__()
        self._session = ClientSession(read, write)
        await self._session.__aenter__()
        await self._session.initialize()
        self._ready.set()

    def stop(self):
        if self._loop:
            self._loop.call_soon_threadsafe(self._loop.stop)
        if self._thread:
            self._thread.join(timeout=5)

    def call_tool(self, name: str, arguments: dict) -> str:
        future = asyncio.run_coroutine_threadsafe(
            self._session.call_tool(name, arguments), self._loop
        )
        result = future.result(timeout=30)
        return extract_text(result)

def extract_text(result) -> str:
    return "\n".join(item.text for item in result.content if hasattr(item, "text"))
