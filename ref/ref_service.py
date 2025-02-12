from asgiref.sync import sync_to_async
from django.utils.timezone import now
from datetime import timedelta
from ref.repository import RefRepo
from users.models import User
from users.repository import UserRepo


class ReferralService:
    @staticmethod
    async def create_referral_code(user: User, duration_days: int):
        """Создаёт реферальный код для пользователя, если его нет"""
        exists = await RefRepo.check_exist_ref_code_by_user(user)
        if exists:
            return {"detail": "Реферальный код уже существует"}
        expires_at = now() + timedelta(days=duration_days)
        ref_code = await RefRepo.create_ref(user=user, expires_at=expires_at)
        return {"ref_code": str(ref_code.ref_code), "expires_at": expires_at}

    @staticmethod
    async def delete_referral_code(user):
        """Удаляет реферальный код, если он есть у пользователя"""
        ref_code = await RefRepo.get_ref_by_filter(user=user)
        if not ref_code:
            return {"detail": "Реферальный код не найден"}
        await ref_code.adelete()
        return {"detail": "Реферальный код удалён"}

    @staticmethod
    async def get_referral_code_by_email(email: str):
        """Получает реферальный код по email пользователя"""
        user = await UserRepo.get_user_by_filters(email=email)
        if not user:
            return {"detail": "Пользователь не найден"}
        ref_code = await RefRepo.get_ref_by_filter(user=user)
        if not ref_code:
            return {"detail": "Реферальный код не найден"}

        return {"ref_code": str(ref_code.ref_code)}

    @staticmethod
    async def register_with_referral_code(ref_code: str, user_name: str, password: str):
        """Регистрирует нового пользователя по реферальному коду"""
        referrer = await RefRepo.get_referrer_by_filter(ref_code=ref_code)
        if not referrer or referrer.is_expired():
            return {"detail": "Реферальный код недействителен или просрочен"}
        user = await UserRepo.create_user(user_name=user_name, password=password, invite_ref_code=ref_code)
        return {"detail": "Пользователь успешно зарегистрирован", "user_id": user.id}

    @staticmethod
    async def get_referrals_by_id(referrer_id: int):
        """Получает всех пользователей, зарегистрированных по реферальному коду данного пользователя"""
        ref_code = await RefRepo.get_referrer_code(user_id=referrer_id)
        if not ref_code:
            return {"detail": "У пользователя нет реферального кода"}
        referrals = await sync_to_async(list)(
            await UserRepo.get_all_users(invite_ref_code=ref_code)
        )
        return referrals
