from django.db import DatabaseError, IntegrityError
from django.forms import model_to_dict
from users.models import User
from asgiref.sync import sync_to_async


class UserRepo:
    @staticmethod
    async def get_all_users(**kwargs):
        """Получает всех пользователей по фильтру"""
        try:
            fields = ["id", "user_name", "role", "email"]

            @sync_to_async
            def fetch_users():
                query = User.objects.filter(**kwargs) if kwargs else User.objects.all()
                return list(query.values(*fields))

            return await fetch_users()
        except DatabaseError as e:
            return {"error": f"Ошибка базы данных при получении пользователей: {str(e)}"}
        except Exception as e:
            return {"error": f"Неизвестная ошибка при получении списка пользователей: {str(e)}"}

    @staticmethod
    async def get_user_by_filters(**filters):
        """Получает пользователя по фильтрам"""
        try:
            return await User.objects.filter(**filters).afirst()
        except Exception as e:
            return {"error": f"Ошибка при получении пользователя: {str(e)}"}

    @staticmethod
    async def create_user(**kwargs):
        """Создает нового пользователя с проверкой уникальности email и user_name"""
        try:
            existing_user = await User.objects.filter(user_name=kwargs.get("user_name")).afirst()
            if existing_user:
                return {"error": "Пользователь с таким именем уже существует"}

            existing_email = await User.objects.filter(email=kwargs.get("email")).afirst()
            if existing_email:
                return {"error": "Пользователь с таким email уже существует"}

            return await User.objects.acreate(**kwargs)
        except IntegrityError:
            return {"error": "Ошибка уникальности. Возможно, пользователь уже существует"}
        except Exception as e:
            return {"error": f"Ошибка при создании пользователя: {str(e)}"}