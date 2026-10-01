import os


class Config:
    SECRET_KEY = os.getenv("LABMOD_SECRET", "change-this-secret")
    DB_HOST = os.getenv("LABMOD_DB_HOST", "127.0.0.1")
    DB_USER = os.getenv("LABMOD_DB_USER", "root")
    DB_PASSWORD = os.getenv("LABMOD_DB_PASSWORD", "")
    DB_NAME = os.getenv("LABMOD_DB_NAME", "laboratry_module_db")
    DB_PORT = int(os.getenv("LABMOD_DB_PORT", "3306"))
    AUTH_DB_HOST = os.getenv("LABMOD_AUTH_DB_HOST", "127.0.0.1")
    AUTH_DB_USER = os.getenv("LABMOD_AUTH_DB_USER", "root")
    AUTH_DB_PASSWORD = os.getenv("LABMOD_AUTH_DB_PASSWORD", "")
    AUTH_DB_NAME = os.getenv("LABMOD_AUTH_DB_NAME", "hiccup_ticket")
    AUTH_DB_PORT = int(os.getenv("LABMOD_AUTH_DB_PORT", "3306"))
