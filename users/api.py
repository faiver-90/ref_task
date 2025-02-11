from asgiref.sync import sync_to_async
from ninja import Router
from auth_custom.sercvices.jwt_service import JWTAuth
from users.repository import UserRepo
from users.schemas import UserSchema, PartialUserSchema
from users.user_service import UserService

user_router = Router(tags=['Users'])


@user_router.post("/create_user", summary="Создать пользователя")
async def create_user(request, data: UserSchema):
    """
    **Создаёт нового пользователя**.

    **Входные данные:**
    - `user_name` (str): Имя пользователя (уникальное).
    - `password` (str): Пароль пользователя.
    - `role` (str): Роль пользователя.
    - `email` (str): Электронная почта пользователя.

    **Ответ:**
    - `detail` (str): Сообщение об успешном создании или ошибка.
    """
    try:
        return await UserService.create_user(data.user_name, data.password, data.role, data.email)
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": "Internal Server Error", "detail": str(e)}


@user_router.put("/update_user/", auth=JWTAuth(), summary="Обновить данные пользователя")
async def update_user(request, data: PartialUserSchema):
    """
    **Обновляет данные пользователя по `user_name`** (требуется аутентификация).

    **Входные данные:**
    - `data` (PartialUserSchema): Поля, которые нужно обновить.

    **Ответ:**
    - `detail` (str): Сообщение об успешном обновлении или ошибка.
    """
    try:
        user_name = request.auth['user_name']
        return await UserService.update_user_by_user_name(user_name, data)
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": "Internal Server Error", "detail": str(e)}


@user_router.get("/get_user_by_token", auth=JWTAuth(), summary="Получить данные текущего пользователя")
async def get_user_by_user_name(request):
    """
    **Возвращает данные текущего аутентифицированного пользователя**.

    **Ответ:**
    - `user_id` (int): ID пользователя.
    - `user_name` (str): Имя пользователя.
    - `email` (str): Электронная почта пользователя.
    - `role` (str): Роль пользователя.
    """
    try:
        return await UserService.get_user_by_user_name(request.auth['user_name'])
    except Exception as e:
        return {"error": "Internal Server Error", "detail": str(e)}


@user_router.delete("/delete_user/{user_id}", auth=JWTAuth(), summary="Удалить пользователя")
async def delete_user(request, user_id: int):
    """
    **Удаляет пользователя по ID** (требуется аутентификация).

    **Входные данные:**
    - `user_id` (int): ID пользователя, которого нужно удалить.

    **Ответ:**
    - `detail` (str): Подтверждение удаления или ошибка.
    """
    try:
        user_id_req = request.auth['user_id']
        return await UserService.delete_user(user_id, user_id_req)
    except Exception as e:
        return {"error": "Internal Server Error", "detail": str(e)}


@user_router.get("/get_users", summary="Получить список всех пользователей")
async def get_users(request):
    """
    **Возвращает список всех пользователей**.

    **Ответ:**
    ```json
    {
        "users": [
            {
                "id": 1,
                "user_name": "admin",
                "email": "admin@example.com"
            },
            {
                "id": 2,
                "user_name": "user1",
                "email": "user1@example.com"
            }
        ]
    }
    ```
    """
    try:
        users = await sync_to_async(list)(await UserRepo.get_all_users())
        return {"users": list(users)}
    except Exception as e:
        return {"error": "Internal Server Error", "detail": str(e)}
