# Generated by Django 4.2.10 on 2024-03-08 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_sectors_cards'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subsectors',
            name='damage_percentage',
            field=models.FloatField(blank=True, null=True, verbose_name='النسبة المئوية'),
        ),
        migrations.AlterField(
            model_name='subsectors',
            name='number',
            field=models.FloatField(blank=True, null=True, verbose_name='الرقم'),
        ),
    ]
