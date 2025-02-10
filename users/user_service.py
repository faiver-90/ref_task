from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from users.models import User


class UserService:
    @staticmethod
    async def create_user(user_name, password, role):
        user = await User.objects.filter(user_name=user_name).afirst()
        if user:
            raise ValueError("User already exist")
        await User.objects.acreate(user_name=user_name, password=password, role=role)

        return {'detail': "User created"}

    @staticmethod
    async def update_user_by_user_name(user_name, data):
        user = await User.objects.filter(user_name=user_name).afirst()
        if not user:
            return JsonResponse({"detail": "User not found"}, status=404)

        for field, value in data.dict(exclude_unset=True).items():
            setattr(user, field, value)
        await user.asave()  # Асинхронное сохранение
        return {'detail': "User updated"}

    @staticmethod
    async def get_user_by_user_name(user_name: str):
        user = await User.objects.filter(user_name=user_name).afirst()
        if not user:
            return {"detail": "User not found"}, 404
        return model_to_dict(user)

    @staticmethod
    async def delete_user(user_id, user_id_req):
        user = await User.objects.filter(id=user_id).afirst()
        if not user:
            return JsonResponse({"detail": "User not found"}, status=404)

        if user.id != user_id_req:
            return JsonResponse({"detail": "Permission denied"}, status=403)

        await user.adelete()
        return {'detail': "User deleted"}
