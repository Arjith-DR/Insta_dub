from user.routers.users import users_router
from user.routers.bios import bios_router
from user.routers.posts import posts_router
from user.routers.reels import reels_router
from user.routers.followers import followers_router

user_routers = [users_router, bios_router, posts_router, reels_router, followers_router]
