# Threat Model

## Assets
Provider/API credentials, user prompts and outputs, model artifacts, MCP tool capabilities, A2A identities, audit records, CI credentials and release artifacts.

## Trust boundaries
1. External users and agents -> OIDC authentication.
2. Gateway -> model provider.
3. Gateway -> MCP servers/tools.
4. Source repository -> CI runners -> build artifacts -> deployment.
5. Model registry -> runtime model loader.

## Threats and controls
- Prompt injection: input policy, tool capability separation, output validation; classifiers are needed beyond regex.
- Unauthorized agent/tool use: short-lived workload identity, issuer/audience validation, scopes, allowlists, deny-by-default.
- MCP tool poisoning / confused deputy: server and tool allowlists, per-tool authorization, schema validation, egress controls, human approval for consequential actions.
- Model tampering: immutable digests, signed artifacts, provenance attestations, registry allowlist, deployment-time verification.
- Dependency compromise: lock dependencies, dependency review, Dependabot, pip-audit, SBOM and provenance.
- Secret leakage: secret manager, Gitleaks, least privilege, rotation, no prompt/token logging.
- CI compromise: protected branches/environments, pinned action SHAs, minimal permissions, isolated runners, required review.

## Residual risks
Regex guardrails are bypassable; model outputs can be unsafe; JWT key rotation and issuer availability require operational design; MCP adapter requires transport-specific security review; CI scanners have false negatives. Perform red-team testing and independent review before production.
