from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Application
    app_name: str = "MS-Order"
    app_version: str = "1.0.0"
    app_description: str = "Microsserviço para gerenciamento de pedidos e catálogo"
    
    # Service configuration
    service_name: str = "ms-order"
    service_port: int = 8001
    service_host: str = "0.0.0.0"
    
    # Database configuration
    database_url: str = "postgresql://order_user:order_pass@localhost:5432/order_db"
    database_echo: bool = False  # Log SQL queries
    database_pool_size: int = 10
    database_max_overflow: int = 20
    
    # New database fields for better configuration
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "order_db"
    db_user: str = "order_user"
    db_password: str = "order_pass"
    db_driver: str = "postgresql+psycopg2"
    db_pool_size: int = 10
    db_max_overflow: int = 20
    db_pool_timeout: int = 30
    db_pool_pre_ping: bool = True
    db_echo: bool = False
    
    # API configuration
    api_v1_prefix: str = "/api/v1"
    docs_url: Optional[str] = "/api/docs"
    redoc_url: Optional[str] = "/api/redoc"
    openapi_url: str = "/api/openapi.json"
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    # CORS
    cors_origins: list = ["*"]
    cors_methods: list = ["*"]
    cors_headers: list = ["*"]
    
    # Catalog initialization
    init_catalog: bool = True
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Security (for future use)
    secret_key: Optional[str] = None
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 30
    
    # Health check
    health_check_interval: int = 30
    
    # External services
    payment_service_url: str = "http://localhost:8002"
    production_service_url: str = "http://localhost:8003"
    catalog_service_url: str = "http://localhost:8001"
    
    # Feature flags
    enable_swagger_ui: bool = True
    enable_redoc: bool = True
    enable_health_check: bool = True
    
    # Request configuration
    request_timeout: int = 30
    max_retries: int = 3
    backoff_factor: float = 0.3
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields to avoid validation errors
        
    @property
    def is_development(self) -> bool:
        return self.environment.lower() in ["development", "dev"]
        
    @property
    def is_production(self) -> bool:
        return self.environment.lower() in ["production", "prod"]
        
    def get_database_url(self) -> str:
        """Get database URL with proper formatting"""
        # If database_url is explicitly set and doesn't contain localhost, use it
        if self.database_url and "localhost" not in self.database_url:
            return self.database_url
        # Otherwise, construct from components
        return f"{self.db_driver}://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        
    def get_docs_config(self) -> dict:
        """Get documentation configuration based on environment"""
        if self.is_production and not self.debug:
            return {
                "docs_url": None,
                "redoc_url": None,
                "openapi_url": None
            }
        return {
            "docs_url": self.docs_url,
            "redoc_url": self.redoc_url,
            "openapi_url": self.openapi_url
        }


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
