import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    REDIS_HOST = 'redis'
    REDIS_PORT = 6379
