from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _
from .models import *


class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model with no username field."""
    fieldsets = (
        (None, {'fields': ('first_name',
                           'last_name',
                           'avatarUrl',
                           'status',
                           'email',
                           'role',
                           'company',
                           'documento',
                           )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'is_staff', 'password1', 'password2'),
        }),
    )

    list_display = ('first_name', 'last_name', 'email',
                    'isVerified', 'role', 'company','documento',)
    search_fields = ('id', 'first_name', 'last_name', 'email','documento')
    ordering = ('id',)
    list_filter = ('is_staff', 'role', 'isVerified', 'company','documento',)


class EventoElectoralAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha', )
    ordering = ('nombre',)
    search_fields = ('nombre',)


class ListaElectoralAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'cab', 'logo_file', )
    ordering = ('nombre',)
    search_fields = ('nombre',)


class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ('nombre', )
    ordering = ('nombre',)
    search_fields = ('nombre',)


class CantonAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'provincia')
    ordering = ('nombre',)
    search_fields = ('nombre',)


class DetPersonaPadronElectoralAdmin(admin.ModelAdmin):
    list_display = ('dni', 'nombre', 'apellido', 'canton', 'cab')
    ordering = ('nombre',)
    search_fields = ('nombre',)


class VotoPersonaPadronAdmin(admin.ModelAdmin):
    list_display = ('persona', 'cab', 'tipo', 'lista',)
    ordering = ('cab',)
    search_fields = ('cab',)



admin.site.register(Canton, CantonAdmin)
admin.site.register(Provincia, ProvinciaAdmin)
admin.site.register(EventoElectoral, EventoElectoralAdmin)
admin.site.register(ListaElectoral, ListaElectoralAdmin)
admin.site.register(DetPersonaPadronElectoral, DetPersonaPadronElectoralAdmin)
admin.site.register(VotoPersonaPadron, VotoPersonaPadronAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
