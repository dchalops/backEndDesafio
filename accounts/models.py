import os

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import UnicodeUsernameValidator
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext as _
import uuid


# This is just an example no need to keep them
ROLE_CHOICES = (

    ('Backend Developer', 'Backend Developer'),
    ('Full Stack Designer', 'Full Stack Designer'),
    ('Front End Developer', 'Front End Developer'),
    ('Full Stack Developer', 'Full Stack Developer'),
)

STATUS_CHOICES = (
    ('active', 'ACTIVE'),
    ('banned', 'BANNED'),
)


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    id = models.UUIDField(primary_key=True, unique=True,
                          default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)

    documento = models.CharField(
        max_length=10, default='999999999', unique=True)

    isVerified = models.BooleanField(default=False)
    avatarUrl = models.ImageField(
        upload_to='users', null=True, blank=True, default='/placeholder.png')
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default='active')
    role = models.CharField(
        max_length=100, choices=ROLE_CHOICES, default='Full Stack Developer')
    company = models.CharField(max_length=100, default='NA')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        ordering = ["-id"]


class EventoElectoral(models.Model):
    nombre = models.CharField(default='', blank=True, null=True, max_length=1000, verbose_name=u'Nombre')
    fecha = models.DateField(blank=True, null=True, verbose_name=u'Fecha Elección')
    
    def __str__(self):
        return f'{self.nombre}'

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper().strip()
        super(EventoElectoral, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u"Padron Electoral"
        verbose_name_plural = u"Padron Electoral"


ESTADO_VOTO = (
    (1, 'Valido'),
    (2, 'Blanco'),
    (3, 'Nulo'),
)


class ListaElectoral(models.Model):
    tipo = models.IntegerField(choices=ESTADO_VOTO, default=1, verbose_name='Tipo Voto')
    nombre = models.CharField(default='', blank=True, null=True, max_length=1000, verbose_name=u'Nombre')
    cab = models.ForeignKey(EventoElectoral, blank=True, null=True, verbose_name=u'Cab', on_delete=models.CASCADE)
    logo = models.CharField(default='', blank=True, null=True, max_length=2000, verbose_name=u'Logo')
    logo_file = models.FileField(default='', blank=True, null=True, max_length=2000, verbose_name=u'Logo File')

    def __str__(self):
        return f'{self.nombre}'

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper().strip()
        super(ListaElectoral, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u"Lista Electoral"
        verbose_name_plural = u"Listas Electorales"


class TablaResultado(models.Model):
    cab = models.ForeignKey(EventoElectoral, blank=True, null=True, verbose_name=u'Cab', on_delete=models.CASCADE)
    empadronado = models.IntegerField(default=0, verbose_name=u"Numero de empadronados")
    ausentismo = models.IntegerField(default=0, verbose_name=u"Votos no utilizados (ausentismo)")
    votovalido = models.IntegerField(default=0, verbose_name=u"Votos total validos")
    votonulo = models.IntegerField(default=0, verbose_name=u"Votos nulos")
    votoblanco = models.IntegerField(default=0, verbose_name=u"Votos blanco")

    def adicional(self):
        return SubTablaResultado.objects.filter(status=True, detallemesa=self).order_by('lista__nombre')

    class Meta:
        verbose_name = u'Detalle Mesa'
        verbose_name_plural = u'Detalles de Mesas'

    def __str__(self):
        return f'{self.mesa_responsable} {self.gremio_periodo} '

    def mis_listas(self):
        return self.gremio_periodo.listagremio_set.filter(status=True)

    def save(self, *args, **kwargs):
        super(TablaResultado, self).save(*args, **kwargs)


class SubTablaResultado(models.Model):
    detallemesa = models.ForeignKey(TablaResultado, blank=True, null=True, verbose_name=u'Detalle de la mesa', on_delete=models.CASCADE)
    lista = models.ForeignKey(ListaElectoral, blank=True, null=True, verbose_name=u'Listas electorales', on_delete=models.CASCADE)
    totalvoto = models.IntegerField(default=0, verbose_name=u"Total de votos")

    class Meta:
        verbose_name = u'SubDetalles Mesa'
        verbose_name_plural = u'SubDetalles de Mesas'

    def __str__(self):
        return f'{self.detallemesa} {self.lista} '

    def save(self, *args, **kwargs):
        super(SubTablaResultado, self).save(*args, **kwargs)


class Provincia(models.Model):
    nombre = models.CharField(default='', blank=True, null=True, max_length=1000, verbose_name=u'Nombre')


class Canton(models.Model):
    nombre = models.CharField(default='', blank=True, null=True, max_length=1000, verbose_name=u'Nombre')
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, blank=True, null=True, max_length=1000, verbose_name=u'Provincia')


class DetPersonaPadronElectoral(models.Model):
    cab = models.ForeignKey(EventoElectoral, blank=True, null=True, verbose_name=u'Cab', on_delete=models.CASCADE)
    dni = models.CharField(default='', blank=True, null=True, max_length=1000, verbose_name=u'DNI')
    nombre = models.CharField(default='', blank=True, null=True, max_length=1000, verbose_name=u'Nombre')
    apellido = models.CharField(default='', blank=True, null=True, max_length=1000, verbose_name=u'Apellido')
    canton = models.ForeignKey(
        Canton, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        max_length=1000, 
        verbose_name=u'Canton'
    )


class VotoPersonaPadron(models.Model):
    tipo = models.IntegerField( choices=ESTADO_VOTO, default=1, verbose_name='Tipo Voto')
    cab = models.ForeignKey(EventoElectoral, blank=True, null=True, verbose_name=u'Cab', on_delete=models.CASCADE)
    persona = models.ForeignKey(DetPersonaPadronElectoral, blank=True, null=True, verbose_name=u'Persona', on_delete=models.CASCADE)
    lista = models.ForeignKey(ListaElectoral, blank=True, null=True, verbose_name=u'Listas electorales', on_delete=models.CASCADE)

