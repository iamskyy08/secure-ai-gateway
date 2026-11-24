import pytest
from fastapi import HTTPException
from app.mcp_proxy import MCPTransport, ToolCall, proxy_tool_call

@pytest.mark.asyncio
async def test_unconfigured_server_fails_closed(monkeypatch):
    monkeypatch.setattr("app.mcp_proxy.settings.allowed_mcp_servers", set())
    with pytest.raises(HTTPException) as exc:
        await proxy_tool_call(ToolCall(server="unknown", tool="read", arguments={}), MCPTransport())
    assert exc.value.status_code == 403
