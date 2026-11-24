# Deployment hardening checklist

- Terminate TLS at a trusted ingress; enforce TLS to providers and MCP servers.
- Store secrets in Vault / cloud secret manager; rotate provider and signing credentials.
- Configure OIDC issuer, audience and JWKS URL; test key rotation and token revocation strategy.
- Use workload identity for service-to-service A2A calls; short TTL and least-privilege scopes.
- Run as non-root, read-only filesystem, seccomp, resource limits, network policies and egress allowlists.
- Pin container base images and GitHub Actions to immutable digests/SHAs.
- Require protected branch, two-person review for policy/model/CI changes, and protected release environment.
- Verify SBOM, provenance and signatures at deploy time; reject unapproved model digests.
- Store audit logs centrally with retention controls; redact sensitive data.
- Add rate limits, quotas, abuse monitoring, tracing and incident response runbooks.
