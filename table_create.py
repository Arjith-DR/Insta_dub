import asyncio
from settings.database import engine, Base
from models import *

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("All tables created successfully!")

if __name__ == "__main__":
    asyncio.run(create_db())