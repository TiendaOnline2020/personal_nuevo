from django.db import models
from django.conf import settings
from personal.models import Persona
# Create your models here.
from twilio.rest import Client
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from email.mime.image import MIMEImage


class Envio_Gmail(models.Model):
    Asunto = models.CharField(max_length=250, verbose_name="Asunto del Mensaje ")
    Cuerpo = models.TextField(verbose_name="Cuerpo del Mensaje ")
    Imagen = models.ImageField(verbose_name="Imagen (opcional)", null=True, blank=True)

    def save(self, *args, **kwargs):
        if settings.MANDAR_MENSAJES_CORREO:
            subject = self.Asunto
            message = self.Cuerpo
            email_from = settings.EMAIL_HOST_USER
            personas = Persona.objects.filter(confirmacion_correo=True)
            recipient_list = [i.correo for i in personas]
            email = EmailMessage(subject, message, email_from, recipient_list)
            email.send()
        super(Envio_Gmail, self).save(*args, **kwargs)

    def __str__(self):
        return self.Asunto
    class Meta:
        verbose_name = "Enviar Mensajes Gmail"


class Envio_Whatsapp(models.Model):
    Asunto = models.CharField(max_length=250, verbose_name="Asunto del Mensaje ")
    Cuerpo = models.TextField(verbose_name="Cuerpo del Mensaje ")
    Imagen = models.ImageField(verbose_name="Imagen (opcional)", null=True, blank=True)

    def save(self, *args, **kwargs):
        if settings.MANDAR_MENSAJES_WSP:
            client = Client(settings.MI_SID_WSP, settings.MI_TOKEN_WSP)
            Mensaje_enviado_Wsp = "Asunto : {} \n {}".format(self.Asunto, str(self.Cuerpo))
            grupo_de_envio = Persona.objects.filter(confirmacion_wsp=True)
            for persona in grupo_de_envio:
                mi_numero = settings.MI_NUMERO_WSP
                numero_a_enviar = settings.NUMERO_DEFAULT_ENVIO + str(persona.telefono)
                message = client.messages.create(
                    from_=mi_numero,
                    body=Mensaje_enviado_Wsp,
                    to=numero_a_enviar
                )
        super(Envio_Whatsapp, self).save(*args, **kwargs)

    def __str__(self):
        return self.Asunto

    class Meta:
        verbose_name = "Enviar Mensajes Whatsapp"
