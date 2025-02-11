from ref.models import RefCode
from users.models import User


class RefRepo:
    @staticmethod
    async def get_ref_by_filter(**kwargs):
        ref_code = await RefCode.objects.filter(**kwargs).afirst()
        return ref_code

    @staticmethod
    async def check_exist_ref_code_by_user(user: User):
        exists = await RefCode.objects.filter(user=user).aexists()
        return exists

    @staticmethod
    async def get_referrer_by_filter(**kwargs):
        referrer = await RefCode.objects.filter(**kwargs).select_related('user').afirst()
        return referrer

    @staticmethod
    async def create_ref(**kwargs):
        ref_code = await RefCode.objects.acreate(**kwargs)
        return ref_code

    @staticmethod
    async def get_referrer_code(**kwargs):
        ref_code = await RefCode.objects.filter(**kwargs).values_list("ref_code", flat=True).afirst()
        return ref_code
