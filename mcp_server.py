from mcp.server import FastMCP
import threading
import asyncio
from typing import Annotated, List
from pydantic import Field, validate_call

from id_mgmt import FidManager, OidManager, TidManager, IdManager, IdType

mcp = FastMCP("romen-mcp",
              port=8000,
              host="127.0.0.1",
              log_level="INFO")

@mcp.tool()
async def gen_fid() -> str:
    """
    Generate a FID
    Returns:
        fid (str): facility id
    """
    return FidManager.generate()
    
@mcp.tool()
async def gen_oid() -> str:
    """
    Generate a OID
    Returns:
        oid (str): Outlet id
    """
    return OidManager.generate()

@mcp.tool()
async def gen_tid() -> List[str]:
    """
    Generate a TID
    Returns:
        tid (str): terminal id
    """
    return TidManager.generate()

@mcp.tool()
@validate_call
async def gen_tids(quantity: Annotated[int, Field(ge=1, le=100)] = 1) -> List[str]:
    """
    Generate multiple TID
    Args:
        quantity (int): number of terminal IDs to generate. Value must be between 1 and 100 (inclusive)
    Returns:
        tid (str): terminal id
    """
    return TidManager.generate(quanity=quantity)

def start_thread():
    asyncio.run(mcp.run_sse_async())

if __name__ == "__main__":
    thread = threading.Thread(target=start_thread)
    thread.start()
