from django.contrib import admin
from .models import Organization, FieldsWork,HeadquarterCountry, Invitation, OrganizationActions
# Register your models here.


admin.site.register(Organization)
admin.site.register(FieldsWork)
admin.site.register(HeadquarterCountry)
admin.site.register(OrganizationActions)
admin.site.register(Invitation)
