from uuid import uuid4
from fastapi import Depends, FastAPI, HTTPException, Request
from app.audit import audit
from app.config import settings
from app.guardrails import check_input, check_output
from app.mcp_proxy import MCPTransport, ToolCall, proxy_tool_call
from app.models import ChatRequest, ChatResponse
from app.provider import generate
from app.security import Principal, require_scope

app = FastAPI(title="Secure AI Gateway", version="0.1.0")
mcp_transport = MCPTransport()

@app.middleware("http")
async def request_size_limit(request: Request, call_next):
    length = request.headers.get("content-length")
    if length and int(length) > settings.max_request_bytes:
        raise HTTPException(status_code=413, detail="Request too large")
    return await call_next(request)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/v1/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest, principal: Principal = Depends(require_scope("ai:invoke"))):
    request_id = str(uuid4())
    incoming = check_input(payload.message)
    if not incoming.allowed:
        audit("input_blocked", principal.subject, request_id, reason=incoming.reason)
        raise HTTPException(status_code=400, detail="Input blocked by policy")
    model = payload.model or settings.model_id
    # Production: require immutable digest identifiers and verify model signatures.
    if settings.allowed_models and model not in settings.allowed_models:
        raise HTTPException(status_code=403, detail="Model is not approved")
    result = await generate(incoming.text, model)
    outgoing = check_output(result, settings.max_output_chars)
    if not outgoing.allowed:
        audit("output_blocked", principal.subject, request_id, reason=outgoing.reason, model=model)
        raise HTTPException(status_code=502, detail="Output blocked by policy")
    audit("inference_allowed", principal.subject, request_id, model=model)
    return ChatResponse(response=outgoing.text, model=model, request_id=request_id)

@app.post("/v1/mcp/tools/call")
async def mcp_call(call: ToolCall, principal: Principal = Depends(require_scope("mcp:tools:call"))):
    request_id = str(uuid4())
    result = await proxy_tool_call(call, mcp_transport)
    audit("mcp_tool_call", principal.subject, request_id, server=call.server, tool=call.tool)
    return result
