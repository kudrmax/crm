from pydantic import PostgresDsn
from sqlalchemy import create_engine


def postgres_url(username, password, host, port, database) -> str:
    return str(PostgresDsn.build(
        scheme="postgresql",
        username=username,
        password=password,
        host=host,
        port=port,
        path=database,
    ))


POSTGRES_URL = postgres_url('postgres', 'postgres', 'localhost', 5533, 'postgres')

engine = create_engine(POSTGRES_URL, future=True, echo=False)
