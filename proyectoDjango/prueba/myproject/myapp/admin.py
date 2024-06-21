from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Ticket, Producto

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'categoria', 'descripcion')
    list_filter = ('categoria',)

class CustomUserAdmin(UserAdmin):
    # Define los campos que deseas mostrar en la lista de usuarios en el admin
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']

# Desregistra el UserAdmin predeterminado y registra el CustomUserAdmin personalizado
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Registra tus otros modelos en el admin
admin.site.register(Producto)
