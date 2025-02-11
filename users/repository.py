from django.forms import model_to_dict

from users.models import User
from asgiref.sync import sync_to_async


class UserRepo:
    @staticmethod
    async def get_all_users(**kwargs):
        field = ["id", "user_name", "role", "email"]
        if kwargs:
            User.objects.filter(**kwargs).values(*field)
        users = User.objects.all().values(*field)
        return users

    @staticmethod
    async def get_user_by_filters(**filters):
        return await User.objects.filter(**filters).afirst()


    @staticmethod
    async def create_user(**kwargs):
        user = await User.objects.acreate(**kwargs)
        return user
