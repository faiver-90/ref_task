from http.client import HTTPException

from django.shortcuts import get_object_or_404
from ninja import Router

from auth_custom.schemas import TokenSchema, LoginSchema, RefreshTokenSchema
from auth_custom.sercvices.jwt_service import get_jwt_service, JWTAuth
from users.models import User

auth_router = Router(tags=['Auth'])

jwt_service = get_jwt_service()


@auth_router.post("/token", response=TokenSchema)
async def login(request, data: LoginSchema):
    user = await User.objects.filter(user_name=data.username, password=data.password).afirst()
    if user is None:
        return {"detail": "Неверные учетные данные"}
    data_for_token = {
        "user_id": user.id,
        "user_role": user.role,
        "user_name": user.user_name,
    }
    access_token = jwt_service.create_access_token(
        {**data_for_token, "type": "access"}, expires_in=3600
    )
    refresh_token = jwt_service.create_access_token(
        {**data_for_token, "type": "refresh"}, expires_in=86400
    )
    await jwt_service.add_tokens_to_user(access_token, data.username, refresh_token)

    return {"access_token": access_token, "refresh_token": refresh_token}


@auth_router.post("/token/refresh", response=TokenSchema)
async def refresh_token(request, data: RefreshTokenSchema):
    try:
        new_access_token = await jwt_service.refresh_access_token(data.refresh_token)
        return {
            "access_token": new_access_token["access_token"],
            "refresh_token": data.refresh_token
        }
    except HTTPException as e:
        return {"detail": str(e)}


@auth_router.get("/validate", auth=JWTAuth())
async def validate_token(request):
    """
    Эндпоинт для проверки токена.
    """
    try:
        return {"valid": True, "payload": request.auth}
    except HTTPException as e:
        return {"valid": False, "detail": str(e)}
