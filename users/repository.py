from django.forms import model_to_dict
from users.models import User
from asgiref.sync import sync_to_async


class UserRepo:
    @staticmethod
    async def get_all_users(**kwargs):
        """Получает всех пользователей по фильтру"""
        try:
            field = ["id", "user_name", "role", "email"]
            if kwargs:
                return await User.objects.filter(**kwargs).values(*field)
            return await User.objects.all().values(*field)
        except Exception as e:
            return {"error": f"Ошибка при получении списка пользователей: {str(e)}"}

    @staticmethod
    async def get_user_by_filters(**filters):
        """Получает пользователя по фильтрам"""
        try:
            return await User.objects.filter(**filters).afirst()
        except Exception as e:
            return {"error": f"Ошибка при получении пользователя: {str(e)}"}

    @staticmethod
    async def create_user(**kwargs):
        """Создает нового пользователя"""
        try:
            return await User.objects.acreate(**kwargs)
        except Exception as e:
            return {"error": f"Ошибка при создании пользователя: {str(e)}"}
