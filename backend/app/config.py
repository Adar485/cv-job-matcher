from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Veritabanı ayarları
    DATABASE_URL: str = "postgresql://postgres:post1234@localhost:5432/cv_job_matcher"
    
    # JWT ayarları
    SECRET_KEY: str = "gizli-anahtar-degistir-bunu-uretimde"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Uygulama ayarları
    APP_NAME: str = "CV Job Matcher"
    DEBUG: bool = True

    class Config:
        env_file = ".env"


settings = Settings()