from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 30
    test_database_url: str = ""
    google_client_id: str = ""
    google_client_secret: str = ""
    github_client_id: str = ""
    github_client_secret: str = ""
    frontend_url: str = "https://ginhu.github.io/Nihongo-Learning"
    cors_origins: str = ""

    model_config = {"env_file": ".env"}

    def get_cors_origins(self) -> list[str]:
        base = [self.frontend_url, "https://ginhu.github.io"]
        if self.cors_origins:
            base += [o.strip() for o in self.cors_origins.split(",") if o.strip()]
        return base


settings = Settings()
