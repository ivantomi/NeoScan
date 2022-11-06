from os import environ


class Config:
    DB_HOST = environ.get("DB_HOST")
    DB_PASSWORD = environ.get("DB_PASSWORD")
    DB_USER = environ.get("DB_USER")
    DB_DATABASE = environ.get("DB_DATABASE")

config = Config()
debug = True