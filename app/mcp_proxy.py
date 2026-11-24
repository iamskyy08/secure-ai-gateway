from fastapi import HTTPException
from pydantic import BaseModel, Field
from app.config import settings

class ToolCall(BaseModel):
    server: str = Field(min_length=1, max_length=100)
    tool: str = Field(min_length=1, max_length=100)
    arguments: dict = Field(default_factory=dict)

class MCPTransport:
    async def call_tool(self, server: str, tool: str, arguments: dict) -> dict:
        # Implement with the official MCP SDK for your transport.
        # Fail closed until a reviewed transport adapter is configured.
        raise HTTPException(status_code=503, detail="MCP transport adapter is not configured")

async def proxy_tool_call(call: ToolCall, transport: MCPTransport):
    if call.server not in settings.allowed_mcp_servers:
        raise HTTPException(status_code=403, detail="MCP server is not allowlisted")
    if call.tool not in settings.allowed_mcp_tools:
        raise HTTPException(status_code=403, detail="MCP tool is not allowlisted")
    if len(str(call.arguments).encode("utf-8")) > 8192:
        raise HTTPException(status_code=413, detail="MCP arguments too large")
    return await transport.call_tool(call.server, call.tool, call.arguments)
