import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ✅ Pull DB URL from .env (required)
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("❌ DATABASE_URL environment variable is not set!")

# ✅ Create Async Engine
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# ✅ Session Factory
SessionLocal = sessionmaker(
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ✅ Base class for models
Base = declarative_base()

# ✅ Async Dependency for FastAPI
async def get_db():
    async with SessionLocal() as session:
        yield session

# ✅ Initialize DB (e.g., from Alembic or manually during dev)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)