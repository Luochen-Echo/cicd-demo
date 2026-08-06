import os

import psycopg

DEFAULT_URL = "postgresql://postgres:test@localhost:5432/postgres"


def get_connection() -> psycopg.Connection:
    url = os.environ.get("DATABASE_URL", DEFAULT_URL)
    return psycopg.connect(url)
