from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = [
        "id",
        "username",
        "email",
        "is_staff",
        "first_name",
        "last_name",
        "phone_number",
    ]

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("email", "first_name", "last_name", "phone_number")}),
    )
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("phone_number",)}),)
