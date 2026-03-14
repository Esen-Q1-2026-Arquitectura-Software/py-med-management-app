import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://med-user:12345@localhost/med-management-db?charset=utf8mb4",
)
JWT_SECRET: str = os.getenv("JWT_SECRET", "dev-jwt-secret")
JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "10"))
JWT_ALGORITHM: str = "HS256"
