import logging
import os
from functools import lru_cache
from pathlib import Path
from typing import List, Optional

from dotenv import load_dotenv
from pydantic import Field, field_validator, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Setup logging for configuration debugging
logger = logging.getLogger(__name__)

# 1. APP_ENV 환경 변수 가져오기 (시스템 환경 변수 또는 기본값)
CURRENT_ENV = os.getenv("APP_ENV", "local")

ROOT_DIR = Path(__file__).resolve().parents[4]

# 2. 환경별 .env 파일 경로 설정
env_file_path = ROOT_DIR / f".env.{CURRENT_ENV}"

print(env_file_path)

load_dotenv(dotenv_path=env_file_path, override=False)

# 3. 환경별 .env 파일이 존재하는지 확인하고 로드
if Path(env_file_path).exists():
    load_dotenv(dotenv_path=env_file_path, override=True)
    logger.info(f"Loading configuration for environment: {CURRENT_ENV}")
    logger.info(f"Environment file loaded: {env_file_path}")
else:
    logger.error(f"Environment file not found: {env_file_path}")
    logger.error(f"Please create {env_file_path} file with required configuration")
    raise FileNotFoundError(f"Required environment file {env_file_path} not found")


class Settings(BaseSettings):
    """Application settings with environment-based configuration."""

    # Application settings
    app_env: str = Field(default=CURRENT_ENV, alias="APP_ENV")
    app_name: str = Field(default="FastAPI-AI", alias="APP_NAME")
    debug: bool = Field(default=False, alias="DEBUG")
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")

    reload: bool = Field(default=False, alias="RELOAD")

    # Database and Redis (required)
    db_url: str = Field(..., alias="DB_URL", description="Database connection URL")
    redis_url: str = Field(..., alias="REDIS_URL", description="Redis connection URL")

    # Security
    secret_key: str = Field(..., alias="SECRET_KEY", min_length=32)

    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    # CORS settings
    allowed_origins: List[str] = Field(default=["*"], alias="ALLOWED_ORIGINS")
    allowed_methods: List[str] = Field(default=["*"], alias="ALLOWED_METHODS")
    allowed_headers: List[str] = Field(default=["*"], alias="ALLOWED_HEADERS")

    # API settings
    api_v1_prefix: str = Field(default="/api/v1", alias="API_V1_PREFIX")
    docs_url: Optional[str] = Field(default="/docs", alias="DOCS_URL")
    redoc_url: Optional[str] = Field(default="/redoc", alias="REDOC_URL")

    # Rate limiting
    rate_limit_per_minute: int = Field(default=60, alias="RATE_LIMIT_PER_MINUTE")

    # Database connection pool settings
    db_pool_size: int = Field(default=20, alias="DB_POOL_SIZE")
    db_max_overflow: int = Field(default=30, alias="DB_MAX_OVERFLOW")

    # Redis connection pool settings
    redis_pool_size: int = Field(default=10, alias="REDIS_POOL_SIZE")

    # JWT settings
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    jwt_expire_minutes: int = Field(default=60, alias="JWT_EXPIRE_MINUTES")

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=str(env_file_path),
        env_file_encoding="utf-8",
        case_sensitive=False,
        validate_assignment=True
    )

    @classmethod
    @field_validator('log_level')
    def validate_log_level(cls, v: str) -> str:
        """Validate log level is one of the standard levels."""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f'log_level must be one of: {valid_levels}')
        return v.upper()

    @classmethod
    @field_validator('allowed_origins', mode='before')
    def parse_allowed_origins(cls, v) -> List[str]:
        """Parse allowed origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v

    @classmethod
    @field_validator('allowed_methods', 'allowed_headers', mode='before')
    def parse_allowed_list(cls, v) -> List[str]:
        """Parse allowed methods/headers from string or list."""
        if isinstance(v, str):
            return [item.strip() for item in v.split(',')]
        return v

    @classmethod
    @field_validator('port')
    def validate_port(cls, v: int) -> int:
        """Validate port is in valid range."""
        if not 1 <= v <= 65535:
            raise ValueError('port must be between 1 and 65535')
        return v

    @computed_field
    @property
    def is_development(self) -> bool:
        """Check if we're in development environment."""
        return self.app_env in ['local', 'dev', 'development']

    @computed_field
    @property
    def is_production(self) -> bool:
        """Check if we're in production environment."""
        return self.app_env in ['prod', 'production']

    @computed_field
    @property
    def server_url(self) -> str:
        """Get the full server URL."""
        protocol = "https" if self.is_production else "http"
        return f"{protocol}://{self.host}:{self.port}"

    def configure_logging(self):
        """Configure application logging based on settings."""
        # logs 디렉토리 생성
        if not self.is_development:
            Path("logs").mkdir(exist_ok=True)

        handlers = [logging.StreamHandler()]
        if not self.is_development:
            handlers.append(logging.FileHandler(f'logs/{self.app_env}.log'))

        logging.basicConfig(
            level=getattr(logging, self.log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=handlers,
            force=True  # 기존 핸들러를 덮어씀
        )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    settings = Settings()

    # Configure logging when settings are first loaded
    settings.configure_logging()

    # Log configuration summary (be careful not to log sensitive data)
    logger.info(f"Application configured for environment: {settings.app_env}")
    logger.info(f"Server will run on: {settings.server_url}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"API prefix: {settings.api_v1_prefix}")

    return settings


# Utility function to validate configuration
def validate_configuration():
    """Validate that all required configuration is present."""
    try:
        settings = get_settings()
        logger.info("Configuration validation successful")
        return True
    except Exception as e:
        logger.error(f"Configuration validation failed: {e}")
        return False


# Environment-specific configuration helpers
def get_database_config():
    """Get database-specific configuration."""
    settings = get_settings()
    return {
        'url': settings.db_url,
        'pool_size': settings.db_pool_size,
        'max_overflow': settings.db_max_overflow,
        'echo': settings.debug,  # Echo SQL queries in debug mode
    }


def get_redis_config():
    """Get Redis-specific configuration."""
    settings = get_settings()
    return {
        'url': settings.redis_url,
        'max_connections': settings.redis_pool_size,
        'decode_responses': True,
    }


def get_cors_config():
    """Get CORS configuration."""
    settings = get_settings()
    return {
        'allow_origins': settings.allowed_origins,
        'allow_methods': settings.allowed_methods,
        'allow_headers': settings.allowed_headers,
        'allow_credentials': True,
    }


# 디버깅을 위한 환경 파일 체크 함수
def check_env_files():
    """Check which environment files exist."""
    possible_envs = ["local", "dev", "development", "staging", "prod", "production"]
    env_files = [f".env.{env}" for env in possible_envs]

    print(f"\n{'=' * 40}")
    print("Environment Files Check")
    print(f"{'=' * 40}")
    print(f"Current working directory: {Path.cwd()}")
    print(f"Current environment: {CURRENT_ENV}")
    print(f"Expected file: .env.{CURRENT_ENV}")
    print()

    for env_file in env_files:
        path = Path(env_file)
        exists = "O" if path.exists() else "X"
        current = " (current)" if env_file == f".env.{CURRENT_ENV}" else ""
        print(f"{exists} {env_file}{current} {'(exists)' if path.exists() else '(not found)'}")
        if path.exists():
            print(f"   Path: {path.absolute()}")

    print(f"{'=' * 40}\n")


# For debugging - use sparingly in production
def print_config_summary():
    """Print configuration summary (excluding sensitive data)."""
    settings = get_settings()

    print(f"\n{'=' * 50}")
    print(f"{settings.app_name} Configuration Summary")
    print(f"{'=' * 50}")
    print(f"Environment: {settings.app_env}")
    print(f"Debug Mode: {settings.debug}")
    print(f"Server: {settings.server_url}")
    print(f"API Prefix: {settings.api_v1_prefix}")
    print(f"Log Level: {settings.log_level}")
    print(f"Allowed Origins: {settings.allowed_origins}")
    print(f"Database Pool Size: {settings.db_pool_size}")
    print(f"Redis Pool Size: {settings.redis_pool_size}")
    print(f"Rate Limit: {settings.rate_limit_per_minute}/min")
    print(f"{'=' * 50}\n")


# 환경 변수 디버깅 함수
def debug_environment():
    """Debug environment variables and files."""
    print(f"\n{'=' * 50}")
    print("Environment Debug Information")
    print(f"{'=' * 50}")

    # 환경 파일 체크
    check_env_files()

    # 주요 환경 변수 체크
    env_vars = ["APP_ENV", "DB_URL", "REDIS_URL", "SECRET_KEY"]
    print("Environment Variables:")
    for var in env_vars:
        value = os.getenv(var)
        if var == "SECRET_KEY" and value:
            print(f"  {var}: {'*' * len(value)} (hidden)")
        elif value:
            print(f"  {var}: {value}")
        else:
            print(f"  {var}: NOT SET")

    print(f"{'=' * 50}\n")
