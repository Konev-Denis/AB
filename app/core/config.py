
from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator

from dotenv import load_dotenv
import os


load_dotenv()
SECRET_JWT = os.environ['SECRET_JWT']


class Settings(BaseSettings):
    PROJECT_NAME: str = "HW"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    DB_HOST: str = ""
    DB_PORT: str = ""
    POSTGRES_DB: str = ""

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
