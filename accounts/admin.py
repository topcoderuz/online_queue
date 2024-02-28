from collections.abc import Sequence
from django.contrib import admin
from django.http.request import HttpRequest
from config.manager import MyDefaultAdmin
from accounts.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'midl_name', 'username', 'phone']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    readonly_fields = ['created_by', 'avatar_tag', 'created', 'updated']
    fieldsets = (
        (None, {
            'fields': (
                ('username', 'phone'),
                ('last_name', 'first_name', 'middle_name',),
                ('jshshir', 'tug_sana', 'passport', 'pass_sana',),
                ('photo', 'avatar_tag',),
                ('created_by', 'created', 'updated'),
            ),
        }),
    )
    def get_list_display(self, request):
        ld = ['get_full_name', 'get_phone', 'is_active', 'is_staff', 'is_superuser' ]
        if request.user.is_super_superuser:
            return ld
        return ld
