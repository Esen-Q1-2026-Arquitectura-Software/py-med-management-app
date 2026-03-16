import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:BackEnd@localhost:5432/postgres",
)
JWT_SECRET: str = os.getenv("JWT_SECRET", "dev-jwt-secret")
JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "10"))
JWT_ALGORITHM: str = "HS256"
