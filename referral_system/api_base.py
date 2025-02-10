from ninja import NinjaAPI

# Инициализация API
from auth_custom.api import auth_router
from users.api import user_router

base_api = NinjaAPI()

base_api.add_router('/users', user_router)
base_api.add_router('/auth', auth_router)
