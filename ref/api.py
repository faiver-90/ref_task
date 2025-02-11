from ninja import Router
from auth_custom.sercvices.jwt_service import JWTAuth
from ref.ref_service import ReferralService
from users.repository import UserRepo

referral_router = Router(tags=["Referral"])


@referral_router.post("/create/", auth=JWTAuth(), summary="Создать реферальный код")
async def create_referral_code(request, duration_days: int):
    """
    **Создать реферальный код для текущего пользователя** (нужна аутентификация).

    **Входные параметры:**
    - `duration_days` (int): Срок действия кода (в днях).

    **Ответ:**
    - `ref_code` (str): Сгенерированный реферальный код.
    - `expires_at` (datetime): Дата истечения кода.
    """
    user = await UserRepo.get_user_by_filters(id=request.auth['user_id'])
    return await ReferralService.create_referral_code(user, duration_days)


@referral_router.delete("/delete/", auth=JWTAuth(), summary="Удалить реферальный код")
async def delete_referral_code(request):
    """
    **Удалить реферальный код пользователя** (нужна аутентификация).

    **Ответ:**
    - `detail` (str): Подтверждение удаления кода.
    """
    user = await UserRepo.get_user_by_filters(id=request.auth['user_id'])
    return await ReferralService.delete_referral_code(user)


@referral_router.get("/get_by_email/", summary="Получить реферальный код по email")
async def get_referral_code_by_email(request, email: str):
    """
    **Получить реферальный код реферера по его email**.

    **Входные параметры:**
    - `email` (str): Email пользователя-реферера.

    **Ответ:**
    - `ref_code` (str): Реферальный код.
    """
    return await ReferralService.get_referral_code_by_email(email)


@referral_router.post("/register/", summary="Регистрация с реферальным кодом")
async def register_with_referral_code(request, ref_code: str, user_name: str, password: str):
    """
    **Регистрация нового пользователя по реферальному коду**.

    **Входные параметры:**
    - `ref_code` (str): Реферальный код, по которому регистрируется пользователь.
    - `user_name` (str): Имя пользователя.
    - `password` (str): Пароль пользователя.

    **Ответ:**
    - `detail` (str): Сообщение об успешной регистрации.
    - `user_id` (int): ID созданного пользователя.
    """
    return await ReferralService.register_with_referral_code(ref_code, user_name, password)


@referral_router.get("/get_referrals_by_id/{referrer_id}", summary="Получить список рефералов")
async def get_referrals_by_id(request, referrer_id: int):
    """
    **Получить список пользователей, зарегистрированных по реферальному коду данного пользователя**.

    **Входные параметры:**
    - `referrer_id` (int): ID пользователя-реферера.

    **Ответ:**
    ```json
    [
        {
            "id": 1,
            "user_name": "referral_1"
        },
        {
            "id": 2,
            "user_name": "referral_2"
        }
    ]
    ```
    """
    return await ReferralService.get_referrals_by_id(referrer_id)
