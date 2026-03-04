from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_instructor', 'is_student', 'is_active')
    list_filter = ('is_instructor', 'is_student', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('is_instructor', 'is_student', 'avatar', 'bio')}),
    )
