from ref.models import RefCode
from users.models import User


class RefRepo:
    @staticmethod
    async def get_ref_by_filter(**kwargs):
        """Получает реферальный код по фильтру"""
        try:
            return await RefCode.objects.filter(**kwargs).afirst()
        except Exception as e:
            return {"error": f"Ошибка при получении реферального кода: {str(e)}"}

    @staticmethod
    async def check_exist_ref_code_by_user(user: User):
        """Проверяет существование реферального кода у пользователя"""
        try:
            return await RefCode.objects.filter(user=user).aexists()
        except Exception as e:
            return {"error": f"Ошибка при проверке реферального кода: {str(e)}"}

    @staticmethod
    async def get_referrer_by_filter(**kwargs):
        """Получает реферера по фильтру"""
        try:
            return await RefCode.objects.filter(**kwargs).select_related('user').afirst()
        except Exception as e:
            return {"error": f"Ошибка при получении реферера: {str(e)}"}

    @staticmethod
    async def create_ref(**kwargs):
        """Создает новый реферальный код"""
        try:
            return await RefCode.objects.acreate(**kwargs)
        except Exception as e:
            return {"error": f"Ошибка при создании реферального кода: {str(e)}"}

    @staticmethod
    async def get_referrer_code(**kwargs):
        """Получает реферальный код реферера"""
        try:
            return await RefCode.objects.filter(**kwargs).values_list("ref_code", flat=True).afirst()
        except Exception as e:
            return {"error": f"Ошибка при получении кода реферера: {str(e)}"}
