from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "user_name", "email", "role", "invite_ref_code")
    search_fields = ("user_name", "email")
    list_filter = ("role",)
