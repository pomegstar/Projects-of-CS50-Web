from django.contrib import admin
from .models import User, Patient
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_doctor', 'is_patient')}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Patient)
