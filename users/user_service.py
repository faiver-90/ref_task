from django.forms import model_to_dict
from django.http import JsonResponse

from users.repository import UserRepo


class UserService:
    @staticmethod
    async def create_user(user_name, password, role, email):
        existing_user = await UserRepo.get_user_by_filters(user_name=user_name)
        if existing_user:
            raise ValueError("Пользователь с таким именем уже существует")

        existing_email = await UserRepo.get_user_by_filters(email=email)
        if existing_email:
            raise ValueError("Пользователь с таким email уже существует")

        await UserRepo.create_user(user_name=user_name, password=password, role=role, email=email)
        return {'detail': "Пользователь создан"}

    @staticmethod
    async def update_user_by_user_name(user_name, data):
        user = await UserRepo.get_user_by_filters(user_name=user_name)

        if not user:
            return {"detail": "Пользователь не найден"}

        for field, value in data.dict(exclude_unset=True).items():
            setattr(user, field, value)
        await user.asave()
        return {'detail': "Пользовательские данные обновлены"}

    @staticmethod
    async def get_user_by_user_name(user_name: str):
        user = await UserRepo.get_user_by_filters(user_name=user_name)

        if not user:
            return {"detail": "Пользователь не найден"}
        return model_to_dict(user)

    @staticmethod
    async def delete_user(user_id, user_id_req):
        user = await UserRepo.get_user_by_filters(id=user_id)

        if not user:
            return JsonResponse({"detail": "Пользователь не найден"}, status=404)

        if user.id != user_id_req:
            return JsonResponse({"detail": "Доступ запрещен"}, status=403)

        await user.adelete()
        return {'detail': "Пользователь удален"}
