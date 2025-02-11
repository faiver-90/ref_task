from asgiref.sync import sync_to_async
from django.forms import model_to_dict
from django.utils.timezone import now
from datetime import timedelta
from ref.models import RefCode
from users.models import User
from ninja.errors import HttpError


class ReferralService:
    @staticmethod
    async def create_referral_code(user: User, duration_days: int):
        """Создаёт реферальный код для пользователя, если его нет"""
        exists = await RefCode.objects.filter(user=user).aexists()
        if exists:
            return {"detail": "Referral code already exists"}

        expires_at = now() + timedelta(days=duration_days)
        ref_code = await RefCode.objects.acreate(user=user, expires_at=expires_at)
        return {"ref_code": str(ref_code.ref_code), "expires_at": expires_at}

    @staticmethod
    async def delete_referral_code(user):
        """Удаляет реферальный код, если он есть у пользователя"""
        ref_code = await RefCode.objects.filter(user=user).afirst()
        if not ref_code:
            return {"detail": "No referral code found"}

        await ref_code.adelete()
        return {"detail": "Referral code deleted"}

    @staticmethod
    async def get_referral_code_by_email(email: str):
        """Получает рефкод по email реферера"""
        user = await User.objects.filter(email=email).afirst()
        if not user:
            return {"detail": "User not found"}

        ref_code = await RefCode.objects.filter(user=user).afirst()
        if not ref_code:
            return {"detail": "No referral code found"}

        return {"ref_code": str(ref_code.ref_code)}

    @staticmethod
    async def register_with_referral_code(ref_code: str, user_name: str, password: str):
        """Регистрирует пользователя по реферальному коду"""
        referrer = await RefCode.objects.filter(ref_code=ref_code).select_related('user').afirst()
        if not referrer or referrer.is_expired():
            return {"detail": "Invalid or expired referral code"}

        user = await User.objects.acreate(user_name=user_name, password=password, invite_ref_code=ref_code)
        return {"detail": "User registered successfully", "user_id": user.id}

    @staticmethod
    async def get_referrals_by_id(referrer_id: int):
        """Получает всех пользователей, зарегистрированных по реферальному коду реферера"""

        # Находим реферальный код, который раздал реферер
        ref_code = await RefCode.objects.filter(user_id=referrer_id).values_list("ref_code", flat=True).afirst()

        if not ref_code:
            return {"detail": "Referrer has no referral code"}

        # Ищем пользователей, зарегистрированных с этим рефкодом
        referrals = await sync_to_async(list)(
            User.objects.filter(invite_ref_code=ref_code).values("id", "user_name")
        )

        return referrals

