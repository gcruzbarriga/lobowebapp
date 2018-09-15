from django.contrib import admin
from control.models import *

class PersonalAdmin(admin.ModelAdmin):
    model = Personal
    list_display = ('nombre', 'apellido_pat', 'sucursal', )

admin.site.register(Personal)
admin.site.register(Sucursal)