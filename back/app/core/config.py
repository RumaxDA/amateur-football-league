from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Wystarczy podać same typy, Pydantic sam wciągnie wartości ze środowiska lub .env
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "db"     # To jest wartość domyślna
    POSTGRES_PORT: int = 5432     # To jest wartość domyślna

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

settings = Settings()