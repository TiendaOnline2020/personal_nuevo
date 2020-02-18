from django.db import models

# Create your models here.
from django.db import models
import requests
from django.conf import settings
# Create your models here.
from smart_selects.db_fields import ChainedForeignKey
from django.core.mail import EmailMessage


class Persona(models.Model):
    numero_dni = models.CharField(max_length=250, verbose_name="Nº de DNI ")
    nombre_persona = models.CharField(max_length=250, verbose_name="Nombres ", null=True, blank=True)
    apellido_paterno = models.CharField(max_length=250, verbose_name="Apellido Paterno ", null=True, blank=True)
    apellido_materno = models.CharField(max_length=250, verbose_name="Apellido Materno ", null=True, blank=True)
    sexo = models.CharField(max_length=250, verbose_name="Sexo ", null=True, blank=True)
    fecha_nacimiento = models.CharField(max_length=250, verbose_name="Fecha de Nacimiento", null=True, blank=True)
    correo = models.EmailField(verbose_name="Correo Electronico", null=True, blank=True)
    imagen = models.ImageField(verbose_name="Imagen de la Persona", null=True, blank=True)
    departamento_persona = models.ForeignKey('departamento', on_delete=models.CASCADE, null=True, blank=True)
    confirmacion_correo = models.BooleanField(null=True, default=False)
    confirmacion_wsp = models.BooleanField(null=True, default=False)
    provincia_persona = ChainedForeignKey(
        'provincia',
        chained_field="departamento_persona",
        chained_model_field="departamento_provincia",
        show_all=False,
        auto_choose=True,
        sort=True
    )
    distrito_persona = ChainedForeignKey(
        'distritos',
        chained_field="provincia_persona",
        chained_model_field="provincia_distrito",
        show_all=False,
        auto_choose=True,
        sort=True
    )
    telefono = models.CharField(max_length=9, null=True, blank=True, verbose_name="Numerode telefono(Opcional)")


    def save(self, *args, **kwargs):

        url = settings.URL_API
        contexto = {
            'strDni': str(self.numero_dni)
        }
        informacion = requests.get(url, contexto).json()['DatosPerson'][0]

        self.apellido_paterno = str(informacion['ApellidoPaterno']).lower().capitalize()
        self.apellido_materno = str(informacion['ApellidoMaterno']).lower().capitalize()

        nombres_separados = informacion['Nombres'].split()
        nombres = ""
        for i in nombres_separados:
            nombres += i.lower().capitalize()
            nombres += " "
        self.nombre_persona = nombres

        if informacion['Sexo'] == '2':
            self.sexo = "Masculino"
        elif informacion['Sexo'] == '3':
            self.sexo = "Femenino"

        numeros_fechas = str(informacion['FechaNacimiento']).split('/')
        mes = settings.DICCIONARIO_MESES[numeros_fechas[1]]
        self.fecha_nacimiento = "{} de {} del {}".format(numeros_fechas[0], mes, numeros_fechas[2])


        if self.telefono:
            self.confirmacion_wsp = True
        if self.correo:
            self.confirmacion_correo = True
        if settings.MANDAR_MENSAJES_CORREO:
            subject = settings.ASUNTO
            message = settings.SALUDO.format(self.nombre_persona) + settings.MENSAJE
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [self.correo]
            email = EmailMessage(subject, message, email_from, recipient_list)
            email.send()
        super(Persona, self).save(*args, **kwargs)


class departamento(models.Model):
    nombre = models.CharField(max_length=250)
    actualizado = models.BooleanField(default=False,null=True,blank=True)
    def __str__(self):
        return self.nombre

class distritos(models.Model):
    nombre = models.CharField(max_length=250)
    provincia_id = models.IntegerField()
    provincia_distrito = models.ForeignKey('provincia', on_delete=models.CASCADE, null=True, blank=True,
                                           verbose_name="Provincia")
    actualizado = models.BooleanField(default=False,null=True,blank=True)
    def __str__(self):
        return self.nombre.lower().capitalize()


class provincia(models.Model):
    nombre = models.CharField(max_length=250)
    departamento_id = models.IntegerField()
    departamento_provincia = models.ForeignKey('departamento', on_delete=models.CASCADE, null=True, blank=True,
                                               verbose_name="Departamento")
    actualizado = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.nombre

class Actualizar(models.Model):
    nombre = models.CharField(max_length=250, null=True, blank=True)
    def save(self, *args, **kwargs):
        mis_provincias = provincia.objects.filter(actualizado=False)
        for provincia_obtenida in mis_provincias:
            provincia_obtenida_objeto = provincia_obtenida
            departamento_obtenido = departamento.objects.get(id=provincia_obtenida_objeto.departamento_id)
            provincia_obtenida_objeto.departamento_provincia = departamento_obtenido
            provincia_obtenida_objeto.save()
        mis_distritos = distritos.objects.filter(actualizado=False)
        for distritos_obtenidos in mis_distritos:
            distrito_objeto = distritos_obtenidos
            provincia_obtenida_distrito = provincia.objects.get(id=distrito_objeto.provincia_id)
            distrito_objeto.provincia_distrito = provincia_obtenida_distrito
            distrito_objeto.save()
        super(Actualizar, self).save(*args, **kwargs)

class todosfalse(models.Model):
    nombre = models.CharField(max_length=250, null=True, blank=True)
    def save(self, *args, **kwargs):
        mis_provincias = provincia.objects.all()
        for provincia_obtenida in mis_provincias:
            provincia_obtenida_objeto = provincia_obtenida
            provincia_obtenida_objeto.actualizado = False
            provincia_obtenida_objeto.save()
        mis_distritos = distritos.objects.all()
        for distritos_obtenidos in mis_distritos:
            distrito_objeto = distritos_obtenidos
            distrito_objeto.actualizado = False
            distrito_objeto.save()
        mis_departamentos = departamento.objects.all()
        for departamentos_obtenido in mis_distritos:
            departamentoobjeto = departamentos_obtenido
            departamentoobjeto.actualizado = False
            departamentoobjeto.save()
        super(todosfalse, self).save(*args, **kwargs)