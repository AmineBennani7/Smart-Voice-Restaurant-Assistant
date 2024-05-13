import os

class Config:
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'rK3#9l!Q@F7h$eGy2Ts%Rw&D4m')

    