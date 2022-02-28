# Create your models here.
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from PIL import Image
from io import BytesIO
from django.core.files import File
from datetime import datetime
from pathlib import Path
from decouple import config


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    company = models.CharField(_('company'), max_length=150, blank=True)
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s ' % self.first_name
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def get_company(self):
        return self.company

    def email_user(self, subject, message, from_email=None, **kwargs):
        """email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class category(models.Model):  # cada alerta tem sua categoria ex: Nonconformity, RedZone, Car ...
    name = models.CharField(default="Nonconformity", max_length=255)
    # slug é tipo um nome mas que pode ser ajustado pra url
    slug = models.SlugField(default="Nonconformity")

    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'


class alert(models.Model):
    # uma categoria pode ter multiplos alertas
    alert_category = models.ForeignKey(category, related_name='alerts', on_delete=models.CASCADE)
    identificador = models.CharField(default="example", max_length=255)
    sequencial = models.IntegerField(default=0)
    slug = models.SlugField(default=f"alerta_example")
    timestamp = models.BigIntegerField(default=1643679950000-(365*24*60*60*1000))
    date_added = models.DateTimeField(auto_now_add=True)
    anotacoes = models.TextField(blank=True, null=True)
    quantidade = models.IntegerField(default=1)
    thumb_up = models.BooleanField(default=False)
    thumb_down = models.BooleanField(default=False)
    # imagem precisa ter campo maior pq as pastas contam
    image = models.ImageField(upload_to='uploads/sauron_imagens/n_avaliadas', blank=True, null=True, max_length=255)
    thumbnail = models.ImageField(upload_to='uploads/sauron_thumbnails/', blank=True, null=True, max_length=255)
    firebase_image_url = models.TextField(default="image_not_sent")
    # desenvolvedor ai colocar imagem na pasta do arquivo abaixo
    local_image_url = models.TextField(default="uploads/sauron_imagens/n_avaliadas/example.png")
    opsreport = models.FileField(upload_to="witsml_opsreports/", default="witsml/opsreport.xml")
    attachment = models.FileField(upload_to="witsml_attachments/", default="witsml/attachment.xml")
    witsml_confirm = models.TextField(default="witsml_not_sent")

    class Meta:
        ordering = ('-date_added',)
    
    def __str__(self):
        return self.identificador

    def get_category_name(self):
        return self.alert_category.name

    def get_absolute_url(self):
        return f'/{self.alert_category.slug}/{self.slug}/'
    
    def get_image(self):
        if self.image:
            # return 'http://192.168.0.27:8000'+self.image.url
            return 'http://'+config('LOCAL_IP', default='127.0.0.1')+':8000' + self.image.url
        return ''

    def get_opsreport(self):
        if self.opsreport:
            return 'http://'+config('LOCAL_IP', default='127.0.0.1')+':8000' + self.opsreport.url

    def get_attachment(self):
        if self.attachment:
            return 'http://'+config('LOCAL_IP', default='127.0.0.1')+':8000' + self.attachment.url

    def get_thumbnail(self):
        if self.thumbnail:
            # return 'http://192.168.0.27:8000'+self.thumbnail.url
            return 'http://'+config('LOCAL_IP', default='127.0.0.1')+':8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return 'http://'+config('LOCAL_IP', default='127.0.0.1')+':8000' + self.thumbnail.url
                # return 'http://192.168.0.27:8000'+self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(180, 120)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, 'PNG', quality=85)
        thumbnail = File(thumb_io, name=Path(image.name).name)
        return thumbnail


class camera(models.Model):
    name = models.CharField(default="camx", max_length=255)
    ativa = models.BooleanField(default=True)
    width = models.BigIntegerField(default = 100)
    height = models.BigIntegerField(default = 100)
    # slug é tipo um nome mas que pode ser ajustado pra url
    slug = models.SlugField(default="camx")

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'


def default_dots():
    # criar uma default red zone
    return [574.84375, 240.5625, 587.84375, 368.5625, 676.84375, 369.5625, 614.84375, 266.5625]


class red_zone(models.Model):
    # uma categoria pode ter multiplos alertas
    red_zone_camera = models.ForeignKey(camera, related_name='red_zones', on_delete=models.CASCADE)
    identificador = models.CharField(default=str(1643679950000-(365*24*60*60)), max_length=255)
    slug = models.SlugField(default=f"red_zone_camx_{1643679950000-(365*24*60*60)}")
    timestamp = models.BigIntegerField(default=1000*(1643679950-(365*24*60*60)))
    date_added = models.DateTimeField(auto_now_add=True)
    name = models.CharField(default=f"example", max_length=255)
    dots = models.JSONField(default=default_dots)
    enabled = models.BooleanField(default=True)
    dots_txt = models.FileField(upload_to=f'uploads/red_zones/individual_red_zones')
    conteudo = models.TextField(default="nome: example, largura: 1980, altura: 1080, pontos: 574.84375,240.5625,587.84375,368.5625,676.84375,369.5625,614.84375,266.5625,")
    local_dots_url = models.TextField(default=f"uploads/red_zones/camx/red_zones_x.txt")  #
    class Meta:
        ordering = ('date_added',)

    def __str__(self):
        return self.identificador

    def get_absolute_url(self):
        return f'/{self.red_zone_camera.slug}/{self.slug}/'

    def get_dots(self):
        if self.dots_txt:
            return 'http://'+config('LOCAL_IP', default='127.0.0.1')+':8000' + self.dots_txt.url
        return ''

    def get_camera(self):
        return self.red_zone_camera.name

    def width(self):
        return self.red_zone_camera.width

    def height(self):
        return self.red_zone_camera.height
