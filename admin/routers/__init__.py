from admin.routers.users import admin_users_router
from admin.routers.roles import admin_roles_router
from admin.routers.privacy import admin_privacy_router


admin_routers = [
    admin_users_router,
    admin_roles_router,
    admin_privacy_router,
]
