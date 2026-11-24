# Model supply-chain policy

1. Ingest models only from approved registries and publishers.
2. Record model name, version, immutable SHA-256 digest, license, source, evaluation results and provenance.
3. Verify publisher signatures and build/download attestations before promotion.
4. Scan model packages and tokenizer/config files; inspect custom code and disable remote code execution by default.
5. Promote through dev -> staging -> production with evaluation gates and human approval.
6. Deploy by digest, never mutable tags; continuously monitor drift and revoke compromised artifacts.
7. Keep model artifacts separate from application dependencies and restrict runtime filesystem/network access.

The starter's allowlist is a guardrail, not a cryptographic signature verifier. Add Sigstore/cosign or your registry's verification mechanism to the release/deployment workflow.
