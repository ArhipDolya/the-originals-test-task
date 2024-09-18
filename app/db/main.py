from app.db.config import get_db_config
from app.db.database import Database

db_config = get_db_config()

database = Database(url=db_config.full_database_url)


async def get_db():
    async with database.get_session() as session:
        yield session
