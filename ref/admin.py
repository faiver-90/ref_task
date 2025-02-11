from django.contrib import admin
from ref.models import RefCode


@admin.register(RefCode)
class RefCodeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "ref_code", "expires_at", "is_expired_status")
    search_fields = ("user__user_name", "ref_code")
    list_filter = ("expires_at",)

    def is_expired_status(self, obj):
        return obj.is_expired()
    is_expired_status.boolean = True
    is_expired_status.short_description = "Expired"
