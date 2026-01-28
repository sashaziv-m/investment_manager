from celery import Celery
from app.core.config import settings

# Redis URL
# If using docker-compose, 'redis' is the hostname from the service name
REDIS_URL = f"redis://:{settings.POSTGRES_PASSWORD}@redis:6379/0" if settings.POSTGRES_PASSWORD else "redis://redis:6379/0"
# Note: For simplicity in this dev setup we are reusing postgres password or assuming none/default. 
# Check docker-compose for actual redis config.
# Ideally we should add REDIS_URL to settings.

# Let's fix the Redis URL logic to use a dedicated env var or a safer default for the compose setup
# In docker-compose.yml we are just running redis:alpine with no password by default usually 
# unless command is overridden.
# We will assume no password for the local dev env as per typical defaults.
CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"

celery_app = Celery("worker", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

celery_app.conf.task_routes = {
    "app.worker.tasks.*": {"queue": "main-queue"},
}

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
