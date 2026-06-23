from core.routers.auth import auth_router
from core.routers.saved import saved_router
from core.routers.content import content_router

core_routers = [auth_router, saved_router, content_router]
