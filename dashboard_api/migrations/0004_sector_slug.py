# Generated by Django 4.2.10 on 2024-02-25 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_api', '0003_alter_action_action_value_alter_action_total_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sector',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
