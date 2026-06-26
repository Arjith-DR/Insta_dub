import asyncio
import traceback
from core.security import verify_password
from user.crud.users import get_users

async def main():
    try:
        users = await get_users()
        print('users', len(users))
        for u in users:
            print(u.user_id, u.email, verify_password('password123', u.password), verify_password('password', u.password))
    except Exception:
        traceback.print_exc()

asyncio.run(main())
