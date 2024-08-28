class Config:
    CELERY_BROKER_URL = 'redis://redis:6379/0'
    RESULT_BACKEND = 'redis://redis:6379/0'
