from ninja import NinjaAPI

# Инициализация API
from auth_custom.api import auth_router
from ref.api import referral_router
from users.api import user_router

base_api = NinjaAPI(
    title="Referral System API",
    version="1.0",
    description="API для работы с пользователями, аутентификацией и реферальной системой.",
    docs_url="/docs",
    openapi_url="/openapi.json",
    auth=None
)

base_api.add_router('/auth', auth_router)
base_api.add_router('/users', user_router)
base_api.add_router('/ref', referral_router)
