import os


class Config:
    SECRET_KEY = os.getenv("LABMOD_SECRET", "change-this-secret")
    DB_HOST = os.getenv("LABMOD_DB_HOST", "host.docker.internal")
    DB_USER = os.getenv("LABMOD_DB_USER", "labmod")
    DB_PASSWORD = os.getenv("LABMOD_DB_PASSWORD", "labmod_pass_123")
    DB_NAME = os.getenv("LABMOD_DB_NAME", "laboratry_module_db")
    DB_PORT = int(os.getenv("LABMOD_DB_PORT", "3310"))
    AUTH_DB_HOST = os.getenv("LABMOD_AUTH_DB_HOST", "host.docker.internal")
    AUTH_DB_USER = os.getenv("LABMOD_AUTH_DB_USER", "root")
    AUTH_DB_PASSWORD = os.getenv("LABMOD_AUTH_DB_PASSWORD", "example")
    AUTH_DB_NAME = os.getenv("LABMOD_AUTH_DB_NAME", "hiccup_ticket")
    AUTH_DB_PORT = int(os.getenv("LABMOD_AUTH_DB_PORT", "8091"))
