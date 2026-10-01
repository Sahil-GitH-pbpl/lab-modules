from contextlib import contextmanager

import pymysql
from flask import current_app


def _connect(host: str, user: str, password: str, database: str, port: int):
    return pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port,
        charset="utf8mb4",
        init_command="SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )


@contextmanager
def get_connection():
    conn = _connect(
        host=current_app.config["DB_HOST"],
        user=current_app.config["DB_USER"],
        password=current_app.config["DB_PASSWORD"],
        database=current_app.config["DB_NAME"],
        port=current_app.config["DB_PORT"],
    )
    try:
        yield conn
    finally:
        conn.close()


@contextmanager
def get_auth_connection():
    conn = _connect(
        host=current_app.config["AUTH_DB_HOST"],
        user=current_app.config["AUTH_DB_USER"],
        password=current_app.config["AUTH_DB_PASSWORD"],
        database=current_app.config["AUTH_DB_NAME"],
        port=current_app.config["AUTH_DB_PORT"],
    )
    try:
        yield conn
    finally:
        conn.close()


def fetch_all(sql: str, params: tuple = ()):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()


def fetch_one(sql: str, params: tuple = ()):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchone()


def fetch_all_auth(sql: str, params: tuple = ()):
    with get_auth_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()


def fetch_one_auth(sql: str, params: tuple = ()):
    with get_auth_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchone()


def execute(sql: str, params: tuple = ()):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
        conn.commit()
