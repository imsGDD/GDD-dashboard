# Generated by Django 4.2.10 on 2024-03-04 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_user_organizations'),
        ('dashboard_api', '0010_alter_action_options_alter_card_options_and_more'),
        ('organizations', '0004_invitation_organization_organizationactions_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Organizations',
        ),
        migrations.AddField(
            model_name='organizationactions',
            name='action',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='action', to='dashboard_api.action', verbose_name='التدخل'),
        ),
        migrations.AddField(
            model_name='organizationactions',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization_action', to='organizations.organization', verbose_name='المنظمة'),
        ),
        migrations.AddField(
            model_name='organization',
            name='fields_work',
            field=models.ManyToManyField(related_name='organization_fieldswork', to='organizations.fieldswork', verbose_name='Fields Work'),
        ),
        migrations.AddField(
            model_name='organization',
            name='headquarter_country',
            field=models.ManyToManyField(related_name='head_quarter_Country', to='organizations.headquartercountry', verbose_name='دولة المقر الرئيسي'),
        ),
        migrations.AddField(
            model_name='invitation',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitations', to='organizations.organization', verbose_name='المنظمة'),
        ),
    ]
