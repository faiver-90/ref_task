import logging
from django.db import IntegrityError
from ninja import Router
from auth_custom.sercvices.jwt_service import JWTAuth
from ref.ref_service import ReferralService
from users.repository import UserRepo

logger = logging.getLogger(__name__)

referral_router = Router(tags=["Referral"], auth=JWTAuth())


@referral_router.post("/create/", summary="Создать реферальный код")
async def create_referral_code(request, duration_days: int):
    """
    Создать реферальный код для текущего пользователя (нужна аутентификация).

    **Входные параметры:**
    - `duration_days` (int): Срок действия кода (в днях).

    **Ответ:**
    - `ref_code` (str): Сгенерированный реферальный код.
    - `expires_at` (datetime): Дата истечения кода.
    """
    try:
        user = await UserRepo.get_user_by_filters(id=request.auth['user_id'])
        return await ReferralService.create_referral_code(user, duration_days)
    except IntegrityError:
        return {"error": "У пользователя уже есть активный реферальный код"}, 400
    except Exception as e:
        logger.exception("Ошибка при создании реферального кода")
        return {"error": "Внутренняя ошибка сервера"}, 500


@referral_router.delete("/delete/", summary="Удалить реферальный код")
async def delete_referral_code(request):
    """
    Удалить реферальный код пользователя (нужна аутентификация).

    **Ответ:**
    - `detail` (str): Подтверждение удаления кода.
    """
    try:
        user = await UserRepo.get_user_by_filters(id=request.auth['user_id'])
        return await ReferralService.delete_referral_code(user)
    except Exception as e:
        logger.exception("Ошибка при удалении реферального кода")
        return {"error": "Внутренняя ошибка сервера"}, 500


@referral_router.get("/get_by_email/", summary="Получить реферальный код по email")
async def get_referral_code_by_email(request, email: str):
    """
    Получить реферальный код реферера по его email.

    **Входные параметры:**
    - `email` (str): Email пользователя-реферера.

    **Ответ:**
    - `ref_code` (str): Реферальный код.
    """
    try:
        return await ReferralService.get_referral_code_by_email(email)
    except Exception as e:
        logger.exception("Ошибка при получении реферального кода по email")
        return {"error": "Внутренняя ошибка сервера"}, 500


@referral_router.post("/register/", summary="Регистрация с реферальным кодом")
async def register_with_referral_code(request, ref_code: str, user_name: str, password: str):
    """
    Регистрация нового пользователя по реферальному коду.

    **Входные параметры:**
    - `ref_code` (str): Реферальный код.
    - `user_name` (str): Имя пользователя.
    - `password` (str): Пароль пользователя.

    **Ответ:**
    - `detail` (str): Сообщение об успешной регистрации.
    - `user_id` (int): ID созданного пользователя.
    """
    try:
        return await ReferralService.register_with_referral_code(ref_code, user_name, password)
    except IntegrityError:
        return {"error": "Пользователь с таким именем уже существует"}, 400
    except Exception as e:
        logger.exception("Ошибка при регистрации с реферальным кодом")
        return {"error": "Внутренняя ошибка сервера"}, 500


@referral_router.get("/get_referrals_by_id/{referrer_id}", summary="Получить список рефералов")
async def get_referrals_by_id(request, referrer_id: int):
    """
    Получить список пользователей, зарегистрированных по реферальному коду данного пользователя.

    **Входные параметры:**
    - `referrer_id` (int): ID пользователя-реферера.

    **Ответ:**
    ```json
    [
        {"id": 1, "user_name": "referral_1"},
        {"id": 2, "user_name": "referral_2"}
    ]
    ```
    """
    try:
        return await ReferralService.get_referrals_by_id(referrer_id)
    except Exception as e:
        logger.exception("Ошибка при получении списка рефералов")
        return {"error": "Внутренняя ошибка сервера"}, 500
