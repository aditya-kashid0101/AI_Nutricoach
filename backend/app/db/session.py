from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

url = make_url(settings.database_url)

engine = create_engine(
    settings.database_url,
    connect_args={"password": url.password} if url.password else {},
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
