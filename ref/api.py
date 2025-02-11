from ninja import Router

from auth_custom.sercvices.jwt_service import JWTAuth
from ref.ref_service import ReferralService
from users.models import User

referral_router = Router(tags=["Referral"])


@referral_router.post("/create/", auth=JWTAuth())
async def create_referral_code(request, duration_days: int):
    """Создать реферальный код (нужна аутентификация)"""
    user = await User.objects.filter(id=request.auth['user_id']).afirst()

    # user = await User.objects.aget(id=request.auth['user_id'])
    return await ReferralService.create_referral_code(user, duration_days)


@referral_router.delete("/delete/", auth=JWTAuth())
async def delete_referral_code(request):
    """Удалить реферальный код"""
    user = await User.objects.aget(id=request.auth['user_id'])
    return await ReferralService.delete_referral_code(user)


@referral_router.get("/get_by_email/")
async def get_referral_code_by_email(request, email: str):
    """Получить реферальный код по email"""
    return await ReferralService.get_referral_code_by_email(email)


@referral_router.post("/register/")
async def register_with_referral_code(request, ref_code: str, user_name: str, password: str):
    """Регистрация с реферальным кодом"""
    return await ReferralService.register_with_referral_code(ref_code, user_name, password)


@referral_router.get("/get_referrals_by_id/{referrer_id}")
async def get_referrals_by_id(request, referrer_id):
    return await ReferralService.get_referrals_by_id(referrer_id)
