from django.db import models
from simple_history.admin import SimpleHistoryAdmin
from datetime import datetime
# from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from simple_history.models import HistoricalRecords
from django.core.validators import RegexValidator

# User = get_user_model()
User = settings.AUTH_USER_MODEL

STATUS_EXAM = (	 
            ('boglanmadi', _("Bog'lanmadi")),	('boglandi', _("Bog'landi")),
            ('kelmadi', _("Kelmadi")),			('keldi', _("Keldi")),
            ('utmadi', _("O'tmadi")),			('utdi', _("O'tdi")),
        )

LANGUAGE_CHOICES = (('uz', _("O'zbek tili")),   ('ru', _("Rus tili")),  ('en', _("Ingliz tili")),)
TALIM_SHAKLI = (    ('1', _("Kunduzgi")),       ('2', _("Kechki")),     ('3', _("Sirtqi")),)

DAYS = (    
        ('0', _("Dushanba")),    ('1', _("Seshanba")),  ('2', _("Chorshanba")),
        ('3', _("Payshanba")),   ('4', _("Juma")),      ('5', _("Shanba")),     ('6', _("Yakshanba")),
    )

TALIM_DARAJASI = (		
                ('11', _("Bakalavr")),                  ('12', _("Magistr")),
                ('10', _("Ikkinchi ta'lim")),           ('13', _("Ordinatura")),
                ('14', _("Doktorantura PhD")),          ('15', _("Doktorantura DSc")),        
            )

EXEM_TYPE_CHOICES = ( ('1', _('Test')),		('2', _('Suhbat')),		('3', _('Diktant')),	('4', _('Insho')),	('5', _('Yozma ish')),	('6', _('Amaliy')), )

today_date = datetime.today().year + 1

EDU_YEAR_CHOICES = [(str(x), f"{x}-{x+1}") for x in range(2023, today_date)]

GENDER_CHOICES = (		('m', _('Erkak')),		('j', _('Ayol')),	)

phoneNumberRegex = RegexValidator(regex = r"^\+\d+$")
phoneNumber = RegexValidator(regex = r"^\+998\d{9}$")
jshshirRegex = RegexValidator(regex = r"^\d{14}$")
innRegex = RegexValidator(regex = r"^\d{9}$")
passportRegex = RegexValidator(regex = r"^[a-zA-Z]{2}\d{7}$")


STATUS_CHOICES = (		('active', _("Faol")),	('arxiv', _("Arxiv")),		('delete', _("O'chirilgan"))	)
class ActiveManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(status='active')

class ArxivManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(status='arxiv')

class DeleteManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(status='delete')

class MyDefaultModel(models.Model):
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active', verbose_name="Holati")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Ro'yxatdan o'tgan vaqti")
    updated = models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan vaqti")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Xodim"))
    history = HistoricalRecords(inherit=True)
    objects = models.Manager()
    active = ActiveManager()
    arxive = ArxivManager()
    delete = DeleteManager()

    class Meta:
        abstract = True
    
    def get_status(self):
        return self.get_status_display()
    get_status.short_description = _("Holati")
    def get_created(self):
        return self.created
    get_created.short_description = _("Qo'shilgan vaqti")
    def get_updated(self):
        return self.updated
    get_updated.short_description = _("Yangilangan vaqti")
    def get_created_by(self):
        return self.created_by.get_full_name()
    get_created_by.short_description = _("Xodim")


class MyDefaultAdmin(SimpleHistoryAdmin):
    actions = []
    date_hierarchy = 'created'
    ordering = '-created',
    save_on_top = True
    list_per_page = 30

    def get_readonly_fields(self, request, obj):
        ro = ['status', 'created_by', 'created', 'updated']
        if request.user.is_super_superuser:
            return ro
        return ro[1:]

    class Media:
        js = ("//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js",)

    def save_model(self, request, obj, form, change):
        if change:
            if not request.user.is_super_superuser:
                obj.created_by = request.user
        else:
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        if request.user.is_super_superuser:
            return super().delete_model(request, obj)
        obj.status = 'delete'
        obj.save()
        return True

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_super_superuser and 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    def has_import_permission(self, request):
        if not request.user.is_superuser:
            return False
        return super().has_import_permission(request)

    # fk qidiruv uchun
    def lookup_allowed(self, key, value):
        check_filter = []
        if key in check_filter:
            return True
        return super(MyDefaultAdmin, self).lookup_allowed(key, value)
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.exclude(status='delete')