import asyncio
import traceback
from user.crud.users import get_users

async def main():
    try:
        users = await get_users()
        print('OK', len(users))
    except Exception:
        traceback.print_exc()

asyncio.run(main())
