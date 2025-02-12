from http.client import HTTPException
from ninja import Router

from auth_custom.schemas import LoginSchema, RefreshTokenSchema
from auth_custom.sercvices.jwt_service import get_jwt_service, JWTAuth
from users.repository import UserRepo

auth_router = Router(tags=['Auth'])

jwt_service = get_jwt_service()


@auth_router.post("/token", summary="Получить JWT токен")
async def login(request, data: LoginSchema):
    """
    **Аутентификация пользователя и получение JWT токенов (access + refresh).**

    **Входные параметры:**
    - `username` (str) - Имя пользователя.
    - `password` (str) - Пароль пользователя.

    **Ответ:**
    - `access_token` (str): JWT-токен для доступа (действителен 1 час).
    - `refresh_token` (str): JWT-токен для обновления (действителен 24 часа).
    """
    try:
        user = await UserRepo.get_user_by_filters(user_name=data.username, password=data.password)
        if user is None:
            raise HTTPException('Неверные учетные данные')

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
    except Exception as e:
        return {"error": "Internal Server Error", "detail": str(e)}


@auth_router.post("/token/refresh", summary="Обновить access токен")
async def refresh_token(request, data: RefreshTokenSchema):
    """
    **Обновление access-токена с использованием refresh-токена.**

    **Входные параметры:**
    - `refresh_token` (str): Действительный refresh-токен.

    **Ответ:**
    - `access_token` (str): Новый JWT-токен доступа.
    - `refresh_token` (str): Текущий refresh-токен (он не обновляется).
    """
    try:
        new_access_token = await jwt_service.refresh_access_token(data.refresh_token)
        return {
            "access_token": new_access_token["access_token"],
            "refresh_token": data.refresh_token
        }
    except HTTPException as e:
        return {"detail": str(e)}
    except Exception as e:
        return {"error": "Internal Server Error", "detail": str(e)}


@auth_router.get("/validate", auth=JWTAuth(), summary="Проверить валидность токена")
async def validate_token(request):
    """
    **Проверка валидности JWT токена.**

    **Ответ:**
    - `valid` (bool): `True`, если токен действителен, иначе `False`.
    - `payload` (dict, optional): Данные токена (если валиден).
    - `detail` (str, optional): Сообщение об ошибке (если токен недействителен).
    """
    try:
        return {"valid": True, "payload": request.auth}
    except HTTPException as e:
        return {"valid": False, "detail": str(e)}
    except Exception as e:
        return {"error": "Internal Server Error", "detail": str(e)}
