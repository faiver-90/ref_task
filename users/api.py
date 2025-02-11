from ninja import Router

from auth_custom.sercvices.jwt_service import JWTAuth
from users.models import User
from users.schemas import UserSchema, PartialUserSchema
from users.user_service import UserService

user_router = Router(tags=['Users'])


@user_router.post("/create_user")
async def create_user(request, data: UserSchema):
    try:
        return await UserService.create_user(data.user_name, data.password, data.role, data.email)
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": "Internal Server Error", "detail": str(e)}


@user_router.put("/update_user/{user_name}", auth=JWTAuth())
async def update_user(request, user_name, data: PartialUserSchema):
    try:
        return await UserService.update_user_by_user_name(user_name, data)
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": "Internal Server Error", "detail": str(e)}


@user_router.get("/get_user_by_token", auth=JWTAuth())
async def get_user_by_user_name(request):
    return await UserService.get_user_by_user_name(request.auth['user_name'])


@user_router.delete("/delete_user/{user_id}", auth=JWTAuth())
async def delete_user(request, user_id):
    user_id_req = request.auth['user_id']
    return await UserService.delete_user(user_id, user_id_req)


@user_router.get("/get_users",)
def get_users(request):
    users = User.objects.all().values("id", "user_name", "role", "email")
    return {"users": list(users)}