from django.contrib import admin
from mainapp.models import ViloyatTuman
from config.manager import MyDefaultAdmin

@admin.register(ViloyatTuman)
class ViloyatTumanAdmin(MyDefaultAdmin):
    search_fields = []

    def get_list_display(self, request):
        ld = ['get_name', 'get_viloyat', 'get_status', 'get_created', 'get_updated', 'get_created_by']
        if request.user.is_super_superuser:
            return ld
        return ld[:-1]