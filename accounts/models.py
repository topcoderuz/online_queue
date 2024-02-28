from django.db import models
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
import uuid

from config.manager import MyDefaultModel, User, STATUS_CHOICES, phoneNumber, passportRegex, jshshirRegex

class Profile(AbstractUser):
    """Foydalanuvchi xodimlar ma'lumotlari"""
    slug = models.UUIDField(default=uuid.uuid4, editable=False)
    middle_name = models.CharField(max_length=255, verbose_name=_("Otasining ismi"), null=True, blank=True)
    phone = models.CharField(validators=[phoneNumber], max_length=13, null=True, blank=True, verbose_name=_("Telefon raqami"))
    passport = models.CharField(validators=[passportRegex], max_length=9, null=True, blank=True, verbose_name=_("Passport"))
    pass_sana = models.DateField(null=True, blank=True, verbose_name=_("Passport berilgan sana"))
    tug_sana = models.DateField(null=True, blank=True, verbose_name=_("Tug'ilgan sana"))
    jshshir = models.CharField(validators=[jshshirRegex], max_length=14, null=True, blank=True,  unique=True, verbose_name=_("JSHSHIR"))
    photo = models.ImageField(upload_to="profile/%Y/%m/%d/", default="profile/nophoto.png", blank=True, verbose_name=_("Rasmi"))
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active', verbose_name=_("Holati"))
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Xodim"))
    created = models.DateTimeField(auto_now_add=True, verbose_name="Ro'yxatdan o'tgan vaqti")
    updated = models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan vaqti")
    is_super_superuser = models.BooleanField(editable=False, default=True, verbose_name=_("Katta xodim"))

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ('-created', )
        verbose_name = _("Xodim")
        verbose_name_plural = _("Xodimlar")

    def __str__(self):
        return self.username

    def get_jshshir(self):
        return self.jshshir
    get_jshshir.short_description = _("JSHSHIR")
    
    def get_full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}" if self.last_name and self.first_name and self.middle_name else f"{self.username}"
    get_full_name.short_description = _("FIO")
    
    def get_phone(self):
        return self.phone
    get_phone.short_description = _("Telefon")
    
    def get_passport(self):
        return self.passport
    get_passport.short_description = _("Passport")
    
    def get_pass_sana(self):
        return self.pass_sana
    get_pass_sana.short_description = _("Passport berilgan sana")
    
    def get_tug_sana(self):
        return self.tug_sana
    get_tug_sana.short_description = _("Tug'ilgan sana")
    
    def avatar_tag(self):
        return mark_safe('<a href="/media/{photo}" target="blank" alt="{name}"> <img src="/media/{photo}" width="50" height="50" /> </a>'.format(
            photo=self.photo, name=self.get_full_name()))
    avatar_tag.short_description = _("Rasm")