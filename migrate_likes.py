import asyncio, sys
sys.path.insert(0, '.')
from dotenv import load_dotenv; load_dotenv()
from settings.database import engine
from sqlalchemy import text

DDL_POST = (
    "CREATE TABLE post_likes ("
    "  like_id SERIAL PRIMARY KEY,"
    "  post_id INTEGER NOT NULL REFERENCES posts(post_id) ON DELETE CASCADE,"
    "  liked_by_user_id INTEGER NOT NULL REFERENCES \"user\"(user_id) ON DELETE CASCADE,"
    "  content_owner_user_id INTEGER,"
    "  liked_at TIMESTAMPTZ DEFAULT now() NOT NULL,"
    "  UNIQUE(post_id, liked_by_user_id)"
    ")"
)

DDL_REEL = (
    "CREATE TABLE reel_likes ("
    "  like_id SERIAL PRIMARY KEY,"
    "  reel_id INTEGER NOT NULL REFERENCES reels(reel_id) ON DELETE CASCADE,"
    "  liked_by_user_id INTEGER NOT NULL REFERENCES \"user\"(user_id) ON DELETE CASCADE,"
    "  content_owner_user_id INTEGER,"
    "  liked_at TIMESTAMPTZ DEFAULT now() NOT NULL,"
    "  UNIQUE(reel_id, liked_by_user_id)"
    ")"
)

async def migrate():
    async with engine.begin() as conn:
        await conn.execute(text("DROP TABLE IF EXISTS post_likes CASCADE"))
        await conn.execute(text("DROP TABLE IF EXISTS reel_likes CASCADE"))
        await conn.execute(text(DDL_POST))
        await conn.execute(text(DDL_REEL))
    print("Tables recreated successfully.")
    await engine.dispose()

asyncio.run(migrate())
