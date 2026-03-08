"""Application configuration"""
import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./dev.db"

    # JWT Authentication
    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_HOURS: int = 24

    # Kubernetes
    K8S_IN_CLUSTER: bool = False

    # Logging
    LOG_LEVEL: str = "INFO"

    # AWS China Region settings
    AWS_REGION: str = os.getenv("AWS_DEFAULT_REGION", "cn-northwest-1")
    AWS_ACCOUNT_ID: str = os.getenv("AWS_ACCOUNT_ID", "")
    AWS_PARTITION: str = os.getenv("AWS_PARTITION", "aws-cn")
    # SQS queue URL — injected at deploy time via env / secret
    SQS_QUEUE_URL: str = os.getenv("SQS_QUEUE_URL", "")
    # ECR registry base — e.g. 735091234506.dkr.ecr.cn-northwest-1.amazonaws.com.cn
    ECR_REGISTRY: str = os.getenv("ECR_REGISTRY", "")
    # Metrics exporter image tag
    METRICS_EXPORTER_TAG: str = os.getenv("METRICS_EXPORTER_TAG", "v0.1.0")

    @property
    def aws_suffix(self) -> str:
        """amazonaws.com for global, amazonaws.com.cn for China"""
        return "amazonaws.com.cn" if self.AWS_PARTITION == "aws-cn" else "amazonaws.com"

    @property
    def bedrock_base_url(self) -> str:
        """Bedrock runtime endpoint (empty for China — Bedrock not available)"""
        if self.AWS_PARTITION == "aws-cn":
            return ""  # Bedrock not available in China regions
        return f"https://bedrock-runtime.{self.AWS_REGION}.{self.aws_suffix}"

    @property
    def ecr_registry_url(self) -> str:
        """Full ECR registry URL"""
        if self.ECR_REGISTRY:
            return self.ECR_REGISTRY
        if self.AWS_ACCOUNT_ID:
            return f"{self.AWS_ACCOUNT_ID}.dkr.ecr.{self.AWS_REGION}.{self.aws_suffix}"
        return ""

    @property
    def metrics_exporter_image(self) -> str:
        """Full metrics exporter image URI"""
        registry = self.ecr_registry_url
        if not registry:
            return ""
        return f"{registry}/openclaw-metrics-exporter:{self.METRICS_EXPORTER_TAG}"


settings = Settings()
