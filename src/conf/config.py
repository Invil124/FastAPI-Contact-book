from pydantic import BaseSettings


class Settings(BaseSettings):
    postgres_url: str = "db_URL"
    secret_key_jwt: str = "secret_key"
    algorithm: str = "HS256"

    mail_username: str = "mail@meta.ua"
    mail_password: str = "password"
    mail_from: str = "mail@meta.ua"
    mail_port: int = 465
    mail_server: str = "smtp.meta.ua"

    redis_host: str = "localhost"
    redis_port: int = 6379

    cloudinary_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
