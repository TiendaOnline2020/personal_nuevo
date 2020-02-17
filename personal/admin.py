from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Persona, departamento, distritos,provincia,Actualizar,todosfalse
class PersonaAdmin(admin.ModelAdmin):
    fields = (
        'numero_dni',
        'correo',
        'imagen',
        'departamento_persona',
        'provincia_persona',
        'distrito_persona',
    )
    list_display = (
        'numero_dni',
        'nombre_persona',
        'apellido_paterno',
        'apellido_materno',
        'sexo',
        'fecha_nacimiento',
        'correo',
        'imagen',
    )

admin.site.register(Persona, PersonaAdmin)
admin.site.register(departamento)
admin.site.register(distritos)
admin.site.register(provincia)
admin.site.register(Actualizar)
admin.site.register(todosfalse)
