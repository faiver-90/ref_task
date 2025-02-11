from django.forms import model_to_dict
from django.http import JsonResponse

from users.repository import UserRepo


class UserService:
    @staticmethod
    async def create_user(user_name, password, role, email):
        user = await UserRepo.get_user_by_filters(user_name=user_name)
        if user:
            raise ValueError("User already exist")
        await UserRepo.create_user(user_name=user_name, password=password, role=role, email=email)
        return {'detail': "User created"}

    @staticmethod
    async def update_user_by_user_name(user_name, data):
        user = await UserRepo.get_user_by_filters(user_name=user_name)

        if not user:
            return {"detail": "User not found"}

        for field, value in data.dict(exclude_unset=True).items():
            setattr(user, field, value)
        await user.asave()
        return {'detail': "User updated"}

    @staticmethod
    async def get_user_by_user_name(user_name: str):
        user = await UserRepo.get_user_by_filters(user_name=user_name)

        if not user:
            return {"detail": "User not found"}, 404
        return model_to_dict(user)

    @staticmethod
    async def delete_user(user_id, user_id_req):
        user = await UserRepo.get_user_by_filters(id=user_id)

        if not user:
            return JsonResponse({"detail": "User not found"}, status=404)

        if user.id != user_id_req:
            return JsonResponse({"detail": "Permission denied"}, status=403)

        await user.adelete()
        return {'detail': "User deleted"}
