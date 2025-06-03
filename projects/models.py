from django.db import models
from django.utils.translation import gettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from organizations.models import Organization
# Create your models here.




class Project(models.Model):
    organization = models.ForeignKey(Organization, related_name='project_organization', null=True, blank=True, on_delete=models.CASCADE, verbose_name=_('Organization Implemented'))
    beneficiary_category = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Beneficiary Category"))
    action_type = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Action Type"))
    #place_implementation = models.CharField(max_length=100, null=True, blank=True, verbose_name=_(" Place Implementation"))
    number_unit = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Number Unit"))
    cost_unit = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Cost Unit"))
    date_implementation = models.DateTimeField(null=True, blank=True, verbose_name=_('Date Implementation'))
    total= models.FloatField(null=True, blank=True,verbose_name=_("Total"))




    class Meta:
        verbose_name = _('Implemented project ')
        verbose_name_plural = _('Implemented projects ')


    def __str__(self):
        return f" {self.beneficiary_category} + {self.action_type}"
    

    def calculate_total(self):
        if self.number_unit is not None and self.cost_unit is not None:
            return float(self.number_unit) * float(self.cost_unit)
        return 0  

@receiver(post_save, sender=Project)
def update_project_total(sender, instance, **kwargs):
    if kwargs.get('created', False): 
        instance.total = instance.calculate_total()
        instance.save(update_fields=['total'])



class PlacesImplementation(models.Model):
    place = models.CharField(max_length=20, verbose_name=_('Name Place'))
    Number = models.IntegerField(default=0,null=True, blank=True, verbose_name=_('Number places'))
    project = models.ForeignKey(Project,related_name='place_project',on_delete=models.CASCADE, verbose_name=_('Place Project'))

    class Meta:
        verbose_name = _('Place Implementation')
        verbose_name_plural = _('Places Implementation')


    def __str__(self):
        return self.place