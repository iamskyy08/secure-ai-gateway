from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_env: str = "development"
    oidc_issuer: str = ""
    oidc_audience: str = "secure-ai-gateway"
    oidc_jwks_url: str = ""
    model_provider_url: str = ""
    model_api_key: str = ""
    model_id: str = "demo-model"
    model_allowlist: str = ""
    max_request_bytes: int = 32768
    max_output_chars: int = 12000
    mcp_allowed_servers: str = ""
    mcp_allowed_tools: str = ""

    @property
    def allowed_models(self) -> set[str]:
        return {x.strip() for x in self.model_allowlist.split(",") if x.strip()}

    @property
    def allowed_mcp_servers(self) -> set[str]:
        return {x.strip() for x in self.mcp_allowed_servers.split(",") if x.strip()}

    @property
    def allowed_mcp_tools(self) -> set[str]:
        return {x.strip() for x in self.mcp_allowed_tools.split(",") if x.strip()}

settings = Settings()
