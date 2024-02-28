from django.db import models
from django.utils.translation import gettext_lazy as _
from config.manager import MyDefaultModel, DAYS
import uuid

class ViloyatTuman(MyDefaultModel):
    """Viloyat va Tumanlar ro'yxati: name, viloyat;"""
    name = models.CharField(_("Nomi"), max_length=150)
    viloyat = models.ForeignKey('self', on_delete=models.CASCADE, related_name="viloyat_tuman", null=True, blank=True, verbose_name=_("Viloyat"))
    
    def get_name(self):
        return self.name
    get_name.short_description = _("Nomi")
    
    def get_viloyat(self):
        try:
            return self.viloyat.get_name()
        except:
            return '-'
    get_viloyat.short_description = _("Viloyat")
    
    def get_tuman_count(self):
        try:
            return self.viloyat_tuman.count()
        except:
            return '-'
    get_tuman_count.short_description = _("Tumanlar soni")
    
    class Meta:
        ordering = '-name',
        verbose_name = _("Viloyat va tuman")
        verbose_name_plural = _("Viloyat va tumanlar")

    def __str__(self):
        return self.name

class Categories(MyDefaultModel):
    """Bo'limlar: name;"""
    name = models.CharField(_("Nomi"), max_length=150)

    def get_name(self):
        return self.name
    get_name.short_description = _("Nomi")
    
    class Meta:
        ordering = '-name',
        verbose_name = _("Bo'limlar")
        verbose_name_plural = _("Bo'limlarlar")

    def __str__(self):
        return self.get_name()

class Organization(MyDefaultModel):
    slug = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(_("Tashkilot nomi"), max_length=255)
    tuman = models.ForeignKey(ViloyatTuman, related_name="org_tuman", verbose_name=_("Tuman"), on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Categories, related_name="org_category", verbose_name=_("Bo'lim"), on_delete=models.SET_NULL, null=True, blank=True)

    def get_name(self):
        return self.name
    get_name.short_description = _("Tashkilot nomi")
    
    def get_tuman(self):
        return self.tuman.get_name()
    get_tuman.short_description = _("Tuman")
    
    def get_category(self):
        return self.category.get_name()
    get_category.short_description = _("Bo'lim")
    
    def __str__(self):
        return self.get_name()
    
    class Meta:
        ordering = "-name",
        verbose_name = _("Tashkilot")
        verbose_name_plural = _("Tashkilotlar")
    

class Services(MyDefaultModel):
    slug = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(_("Xizmat nomi"), max_length=255)

    def get_name(self):
        return self.name
    get_name.short_description = _("Xizmat nomi")
    def __str__(self):
        return self.get_name()

    class Meta:
        ordering = "-name",
        verbose_name = _("Xizmat")
        verbose_name_plural = _("Xizmatlar")
class OrgService(MyDefaultModel):
    slug = models.UUIDField(default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, related_name="orgservice_org", verbose_name=_("Tashkilot"), on_delete=models.CASCADE)
    service = models.ForeignKey(Services, related_name="org_service_service", verbose_name=_("Xizmat"), on_delete=models.CASCADE)
    service_duration = models.IntegerField(_("Xizmat davomiyligi (min)"), default=60)

    def get_name(self):
        return self.service.get_name()
    get_name.short_description = _("Xizmat nomi")
    
    def get_service_duration(self):
        return self.service_duration
    get_service_duration.short_description = _("Xizmat davomiyligi (min)")
    
    def __str__(self):
        return self.get_name()
    
    class Meta:
        ordering = "-organization__name", "-service__name"
        verbose_name = _("Tashkilot xizmatlari")
        verbose_name_plural = _("Tashkilotlar xizmatlari")

class DayOff(MyDefaultModel):
    slug = models.UUIDField(default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, related_name="dayoff_org", verbose_name=_("Tashkilot"), on_delete=models.CASCADE)
    day = models.CharField(_("Hafta kuni"), choices=DAYS, default="6", max_length=1)
    start = models.TimeField(_("...dan"))
    end = models.TimeField(_("...gacha"))

    def get_name(self):
        return self.name
    get_name.short_description = _("Xizmat nomi")
    
    def __str__(self):
        return self.get_name()
    
    class Meta:
        ordering = "-day", "-start", "-organization__name"
        verbose_name = _("Tashkilot xizmatlari")
        verbose_name_plural = _("Tashkilotlar xizmatlari")