from django.db import models
from django.utils.translation import gettext as _

# Create your models here.


class Sectors(models.Model):
    key = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("Key"))
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Name"))
    relief = models.FloatField(verbose_name=_("Relief"))
    recovery = models.FloatField(verbose_name=_("Recovery"))
    development = models.FloatField(verbose_name=_("Development"))
    #cards =  models.ManyToManyField('Cards', related_name='sector_cards',blank=True, verbose_name=_("Sector Cards"))


    class Meta:
        verbose_name = _('Sector')
        verbose_name_plural = _('Sectors')

    def __str__(self):
        return self.name_ar   

 

class SubSectors(models.Model):
    key = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("Key"))
    main_sector=  models.ForeignKey(Sectors, on_delete=models.CASCADE, related_name='main_sector')
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Name"))
    number = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("Number"))
    damage_percentage = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("Damage Percentage"))
    text= models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Text"))
    design_shape= models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Design Shape"))

    class Meta:
        verbose_name = _('Sub Sectors main page')
        verbose_name_plural = _('Sub Sectors main page')

    def __str__(self):
        return self.name_ar    

      


from django.core.exceptions import ValidationError
from datetime import datetime

class LastUpdated(models.Model):
    date = models.DateField(null=True, blank=True, verbose_name=_('Date'))
    time = models.TimeField(null=True, blank=True, verbose_name=_('Time'))

    class Meta:
        verbose_name = _('Last Updated')
        verbose_name_plural = _('Last Updated')
    def __str__(self):
        #return self.date
        return str(self.date) + ' ' + str(self.time)    
    
class Hero(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Name"))
    number = models.IntegerField(null=True, blank=True, verbose_name=_("Number"))

    class Meta:
        verbose_name = _('Hero')
        verbose_name_plural = _('Hero')
        
    def __str__(self):
        return self.name_ar     

class News(models.Model):
    news = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('news'))
    days_of_genocide = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Days of genocide'))
    
    class Meta:
        verbose_name = _('News')
        verbose_name_plural = _('News')

    def __str__(self):
        return self.news_ar


class SummaryTotal(models.Model):
    relief = models.FloatField(verbose_name=_("Relief"))
    recovery = models.FloatField(verbose_name=_("Recovery"))
    development = models.FloatField(verbose_name=_("Development"))
    total= models.FloatField(verbose_name=_("Total"))

    class Meta:
        verbose_name = _('Summary Total Value ')
        verbose_name_plural = _('Summary Total Value ')


    def __str__(self):
        return self.total    















