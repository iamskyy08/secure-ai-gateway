# Secure AI Gateway

A reference implementation of a policy-enforcing AI gateway with input/output guardrails, workload identity for A2A, authorization, an MCP proxy, model supply-chain controls, and CI/CD security checks.

> **Security status:** starter/reference implementation, not a production-certified security boundary. Integrate a real OIDC issuer, secret manager, policy engine, model registry, and security review before production use.

## Capabilities
- FastAPI gateway with request validation, input/output policy checks, provider abstraction, and audit events.
- JWT verification against an OIDC JWKS endpoint; issuer, audience, expiry and signature are checked.
- A2A-style service identity and action-level authorization using scopes and an explicit policy map.
- MCP proxy with server/tool allowlists, argument size limits, timeout, and deny-by-default routing.
- Model registry manifest with immutable digest pinning and an allowlist.
- GitHub Actions CI: tests, Ruff, Bandit, pip-audit, Gitleaks, CodeQL, Trivy filesystem scan, and SBOM generation.
- Dependabot, CODEOWNERS, security policy, threat model and deployment guidance.

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
uvicorn app.main:app --reload
```
Health: `GET /health`. The `/v1/chat` route requires a valid bearer token and a configured model provider.

## Configuration
See `.env.example`. Set `OIDC_ISSUER`, `OIDC_AUDIENCE`, `OIDC_JWKS_URL`, `MODEL_PROVIDER_URL`, and `MODEL_API_KEY` in a secret manager. Never commit credentials.

`MODEL_ALLOWLIST` is a comma-separated list of `provider/model@sha256:<64-hex-digest>` identifiers. Production should resolve model artifacts by immutable digest and verify signatures/attestations before deployment.

## Authentication and authorization
Tokens must be issued by the configured OIDC issuer and contain the configured audience. The `scope` claim is used for route-level authorization. A2A callers should use short-lived workload tokens (for example, SPIFFE/SPIRE-issued identity exchanged through an OIDC-compatible STS). Do not accept caller-supplied identity headers as proof of identity.

Example scopes:
- `ai:invoke` — call model inference
- `mcp:tools:read` — list allowed MCP tools
- `mcp:tools:call` — invoke an allowed MCP tool

## Guardrails
The included deterministic rules are deliberately simple examples. Replace/augment them with a tested policy engine and domain-specific classifiers. Treat model output and tool results as untrusted. Do not rely on prompt instructions as a security control.

## MCP proxy
The proxy only routes to configured servers and tools. Implement the `MCPTransport` adapter for your chosen MCP SDK/transport. The default adapter is intentionally non-functional and fails closed; it does not silently connect to arbitrary URLs.

## CI/CD supply-chain controls
- Pin GitHub Actions to full commit SHAs before production use (the workflow uses major tags for readability in this starter).
- Enable branch protection, required reviews, CODEOWNERS, secret scanning, Dependabot alerts and artifact attestations.
- Generate and sign SBOM/provenance; verify model and container signatures at deploy time.
- Use least-privilege GitHub token permissions and protected environments.
- Review scanner findings; passing CI is not a security certification.

## Run tests
```bash
pytest
ruff check .
bandit -r app
```

## Architecture
```text
Client/Agent -> OIDC JWT -> AI Gateway -> Input Policy -> Model Adapter
                                  |              |
                                  |              v
                                  |         Output Policy -> Client
                                  |
                                  +-> A2A Authorization
                                  +-> MCP Proxy -> allowlisted MCP server/tools
                                  +-> Audit events
CI/CD -> SAST + dependency/secrets/container scans + SBOM -> signed release -> deploy verification
```
