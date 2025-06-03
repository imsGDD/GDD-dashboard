from django.db import models
from django.utils.translation import gettext as _
import uuid
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from uuid import uuid4
from django.utils import timezone
from datetime import timedelta
from dashboard_api.models import Action


class Organization(models.Model):
    name = models.CharField(max_length=150, verbose_name=_('Name'))
    type_organization = models.CharField(max_length=150, verbose_name=_('Type of Organization'))
    email = models.EmailField(max_length=150, verbose_name=_('Email'))
    number_phone = models.CharField(max_length=150, verbose_name=_('Phone Number'))
    website = models.URLField(verbose_name=_('Website'))
    name_person = models.CharField(max_length=150, verbose_name=_('Name of responsible person'))
    job_title = models.CharField(max_length=150, verbose_name=_('Job title'))
    number_whatsup = models.CharField(max_length=150, verbose_name=_('Number Whats Up'))
    country = models.CharField(max_length=150, verbose_name=_('Country'))
    headquarter_country = models.ManyToManyField('HeadquarterCountry', related_name='head_quarter_Country', verbose_name=_('Headquarter Country'))
    fields_work = models.ManyToManyField('FieldsWork', related_name='organization_fieldswork', verbose_name=_('Fields Work'))

    class Meta:
        verbose_name = _('Organization')
        verbose_name_plural = _('Organizations')

    def __str__(self):
        return self.name
    
    


class HeadquarterCountry(models.Model):
    country= models.CharField(max_length=150)
    def __str__(self):
        return self.country
    
    class Meta:
        verbose_name = _('Headquarter Country')
        verbose_name_plural = _('Headquarter Country')

class FieldsWork(models.Model):
    name= models.CharField(max_length=150)

    class Meta:
        verbose_name = _('Fields Work')
        verbose_name_plural = _('FieldsWork')

    def __str__(self):
        return self.name
    

################################################################################


class Invitation(models.Model):
    email = models.EmailField(null=True, blank=True , verbose_name=_("Email"))
    organization = models.ForeignKey(Organization, related_name='invitations', on_delete=models.CASCADE,verbose_name = _('Organization'))
    accepted = models.BooleanField(default=False,  verbose_name=_("Accepted"))
    otp = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("OTP"))
    expire_date = models.DateTimeField(null=True, blank=True, verbose_name=_("Expire Date"))

    class Meta:
        verbose_name = _('Invitations')
        verbose_name_plural = _('Invitations')


    def set_expire_date(self):
        self.expire_date = timezone.now() + timedelta(days=2)
        self.save()


################################################################################


class OrganizationActions(models.Model):
    organization= models.ForeignKey(Organization, related_name='organization_action', on_delete=models.CASCADE,verbose_name = _('Organization'))
    action= models.ForeignKey(Action, related_name='action', on_delete=models.CASCADE,verbose_name = _('Action'))
    action_type = models.CharField(max_length=255, verbose_name=_("Action Type"))

    finished = models.FloatField(null=True, blank=True, verbose_name=_("Finished"))
    finished_percentage = models.FloatField(null=True, blank=True, verbose_name=_("Finished Percentage"))

    
     
    class Meta:
        verbose_name = _('Organization Actions')
        verbose_name_plural = _('Organizations Actions')

    def __str__(self):
        return self.organization.name
    
