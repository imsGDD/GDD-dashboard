# Generated by Django 4.2.10 on 2024-02-28 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organizations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('type_organization', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=150)),
                ('number_phone', models.CharField(max_length=150)),
                ('website', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='HeadquarterCountry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=150)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization_Headquarter_country', to='organizations.organizations')),
            ],
        ),
        migrations.CreateModel(
            name='FieldsWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization_field_work', to='organizations.organizations')),
            ],
        ),
        migrations.CreateModel(
            name='Countries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=150)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization_country', to='organizations.organizations')),
            ],
        ),
    ]
