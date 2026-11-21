import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing from .env")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False
)


def test_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version()"))

        print("PostgreSQL connection successful!")
        print(result.scalar())


if __name__ == "__main__":
    test_connection()
