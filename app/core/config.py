from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Генератор графиков формул"
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True

    # Параметры по умолчанию для формул
    default_linear_k: float = 1.0
    default_linear_b: float = 0.0
    default_quadratic_a: float = 1.0
    default_quadratic_b: float = 0.0
    default_quadratic_c: float = 0.0
    default_exponential_a: float = 1.0
    default_exponential_b: float = 0.1

    class Config:
        env_prefix = "GRAPH_"
        case_sensitive = False

settings = Settings()