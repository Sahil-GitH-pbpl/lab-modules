import os


class Config:
    SECRET_KEY = os.getenv("LABMOD_SECRET", "change-this-secret")
    DB_HOST = os.getenv("LABMOD_DB_HOST", "192.168.0.167")
    DB_USER = os.getenv("LABMOD_DB_USER", "sahil")
    DB_PASSWORD = os.getenv("LABMOD_DB_PASSWORD", "sahil@123")
    DB_NAME = os.getenv("LABMOD_DB_NAME", "creoianw_bhasin")
    DB_PORT = int(os.getenv("LABMOD_DB_PORT", "3306"))
    AUTH_DB_HOST = os.getenv("LABMOD_AUTH_DB_HOST", "192.168.0.173")
    AUTH_DB_USER = os.getenv("LABMOD_AUTH_DB_USER", "root")
    AUTH_DB_PASSWORD = os.getenv("LABMOD_AUTH_DB_PASSWORD", "example")
    AUTH_DB_NAME = os.getenv("LABMOD_AUTH_DB_NAME", "hiccup_ticket")
    AUTH_DB_PORT = int(os.getenv("LABMOD_AUTH_DB_PORT", "8091"))
