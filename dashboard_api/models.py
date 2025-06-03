
    
from django.db import models
from django.utils.translation import gettext as _
from django.dispatch import receiver
from django.db.models import Sum
from django.db.models.signals import post_save

class Sector(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Sector')
        verbose_name_plural = _('Sectors')


class Tag(models.Model):
    name = models.CharField(max_length=20, verbose_name=_('Name'))

    def __str__(self):
        return self.name_ar

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')


class Action(models.Model):
    key = models.CharField(max_length=10, verbose_name=_('Key'))
    sector = models.ForeignKey(Sector, related_name='sector_action', on_delete=models.CASCADE, verbose_name=_('Sector'))
    damage = models.CharField(max_length=255, verbose_name=_('Damage'))
    sub_sector = models.CharField(max_length=255, verbose_name=_('Sub-sector'))
    subclassification = models.CharField(max_length=255, verbose_name=_('Sub-classification'))
    target_number = models.FloatField(verbose_name=_('Target Number'))
    total_estimation = models.FloatField(verbose_name=_('Total Estimation'))
    action_type = models.CharField(max_length=255, verbose_name=_('Action Type'))
    action_value = models.FloatField(null=True, blank=True, verbose_name=_('Action Value'))
    total = models.FloatField(null=True, blank=True, verbose_name=_('Total'))
    tags = models.ManyToManyField(Tag, related_name='actions_tags', verbose_name=_('Tags'))
    finished = models.FloatField(null=True, blank=True, verbose_name=_('Finished'))
    finished_percentage = models.FloatField(null=True, blank=True, verbose_name=_('Finished Percentage'))

    def __str__(self):
        return self.damage_ar

    class Meta:
        verbose_name = _('Action')
        verbose_name_plural = _('Actions')


class ChildAction(models.Model):
    parent_action = models.ForeignKey(Action, on_delete=models.CASCADE, related_name='children', verbose_name=_('Parent Action'))
    key = models.CharField(max_length=10, verbose_name=_('Key'))
    target_number = models.FloatField(verbose_name=_('Target Number'))
    total_estimation = models.FloatField(verbose_name=_('Total Estimation'))
    action_type = models.CharField(max_length=255, verbose_name=_('Action Type'))
    action_value = models.FloatField(null=True, blank=True, verbose_name=_('Action Value'))
    total = models.FloatField(null=True, blank=True, verbose_name=_('Total'))
    tags = models.ManyToManyField(Tag, related_name='child_actions_tags', verbose_name=_('Tags'))
    finished = models.FloatField(null=True, blank=True, verbose_name=_('Finished'))
    finished_percentage = models.FloatField(null=True, blank=True, verbose_name=_('Finished Percentage'))

    def __str__(self):
        return self.action_type_ar

    class Meta:
        verbose_name = _('Child Action')
        verbose_name_plural = _('Child Actions')


class Costs(models.Model):
    key = models.CharField(max_length=10, verbose_name=_('Key'))
    sector = models.ForeignKey(Sector, related_name='sector_cost', on_delete=models.CASCADE, verbose_name=_('Sector'))
    damage_summary = models.CharField(max_length=255, verbose_name=_('Damage Summary'))
    sub_sector = models.CharField(max_length=255, verbose_name=_('Sub-sector'))
    scope_of_intervention = models.TextField(max_length=600, verbose_name=_('Scope of Intervention'))
    relief = models.FloatField(verbose_name=_('Relief'))
    recovery = models.FloatField(verbose_name=_('Recovery'))
    development = models.FloatField(verbose_name=_('Development'))
    total = models.FloatField(verbose_name=_('Total'))

    def __str__(self):
        return self.damage_summary_ar

    class Meta:
        verbose_name = _('Damage Summary')
        verbose_name_plural = _('Damage Summary')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.update_summary()

    def update_summary(self):
        total_relief = Costs.objects.filter(sector=self.sector).aggregate(total_relief=Sum('relief'))['total_relief'] or 0
        total_recovery = Costs.objects.filter(sector=self.sector).aggregate(total_recovery=Sum('recovery'))['total_recovery'] or 0
        total_development = Costs.objects.filter(sector=self.sector).aggregate(total_development=Sum('development'))['total_development'] or 0

        summary_obj, _ = Summary.objects.get_or_create(sector=self.sector)

        summary_obj.relief = total_relief
        summary_obj.recovery = total_recovery
        summary_obj.development = total_development
        summary_obj.total = total_relief + total_recovery + total_development
        summary_obj.save()    


class Summary(models.Model):
    sector = models.ForeignKey(Sector, related_name='sector_summary', on_delete=models.CASCADE, verbose_name=_('Sector'))
    cost = models.ManyToManyField(Costs, related_name='cost_summary', null=True, blank=True, verbose_name=_('Cost'))
    relief = models.FloatField(verbose_name=_('Relief'))
    recovery = models.FloatField(verbose_name=_('Recovery'))
    development = models.FloatField(verbose_name=_('Development'))
    total = models.FloatField(verbose_name=_('Total'))

    def __str__(self):
        return f" summary {self.sector}"

    class Meta:
        verbose_name = _('Summary')
        verbose_name_plural = _('Summaries')
@receiver(post_save, sender=Costs)
def update_summary(sender, instance, **kwargs):
    instance.update_summary()

class DamageReport(models.Model):
    key = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Key'))
    sector = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Sector'))
    sub_sector = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Sub-sector'))
    sub_classification = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Sub-classification'))
    damage_sector = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Damage Sector'))
    damage = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Damage'))
    damage_value_type = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Damage Value Type'))
    damage_value_number = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Damage Value Number'))
    damage_value_percentage = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Damage Value Percentage'))
    updated_at = models.DateField(null=True, blank=True, verbose_name=_('Updated At'))

    class Meta:
        verbose_name = _('Damage Report')
        verbose_name_plural = _('Damage Reports')
    def __str__(self):
        return self.damage_ar       


class Card(models.Model):
    damage_report = models.ForeignKey(DamageReport, on_delete=models.CASCADE, related_name='cards', verbose_name=_('Damage Report'))
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Title'))

    class Meta:
        verbose_name = _('Card')
        verbose_name_plural = _('Cards')
    def __str__(self):
        return self.title_ar       


class Chart(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='charts', verbose_name=_('Card'))
    type = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Type'))
    icon_code = models.TextField(null=True, blank=True, verbose_name=_('Icon Code'))

    class Meta:
        verbose_name = _('Chart')
        verbose_name_plural = _('Charts')
    # def __str__(self):
    #     return self.type_ar  
    def __str__(self):
        return f"{self.type_ar} - {self.card.title_ar}  - {self.id}"         


class ChartData(models.Model):
    chart = models.ForeignKey(Chart, on_delete=models.CASCADE, related_name='data', verbose_name=_('Chart'))
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Name'))
    data_type = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Data Type'))
    #number = models.IntegerField(null=True, blank=True, verbose_name=_('Number'))
    number = models.CharField(max_length=100,null=True, blank=True, verbose_name=_('Number'))

    percentage = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Percentage'))
    updated_at = models.DateField(null=True, blank=True, verbose_name=_('Updated At'))

    class Meta:
        verbose_name = _('Chart Data')
        verbose_name_plural = _('Chart Data')

    def __str__(self):
        return self.name_ar   



