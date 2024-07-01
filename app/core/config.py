import os

class Settings:
    DB_HOST: str = os.getenv("DB_HOST", "172.17.0.1")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_NAME: str = os.getenv("DB_NAME", "your_database_name")
    DB_USER: str = os.getenv("DB_USER", "your_username")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "your_password")

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()
