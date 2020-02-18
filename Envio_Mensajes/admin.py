from django.contrib import admin
from .models import Envio_Gmail, Envio_Whatsapp
# Register your models here.
admin.site.register(Envio_Gmail)
admin.site.register(Envio_Whatsapp)
