from django.contrib import admin
from .models import Sectors, SubSectors, LastUpdated, Hero,SummaryTotal,News
# Register your models here.
from modeltranslation.admin import TranslationAdmin

class SectorsAdmin(TranslationAdmin):
    pass

class SubSectorsAdmin(TranslationAdmin):
    pass
class HeroAdmin(TranslationAdmin):
    pass
class NewsAdmin(TranslationAdmin):
    pass



#################
admin.site.register(Sectors,SectorsAdmin)
admin.site.register(SubSectors,SubSectorsAdmin)
admin.site.register(Hero,HeroAdmin)
admin.site.register(LastUpdated)
admin.site.register(SummaryTotal)
admin.site.register(News,NewsAdmin)

# admin.site.register(Sectors)
# admin.site.register(SubSectors)
# admin.site.register(Hero)
# admin.site.register(LastUpdated)
# admin.site.register(SummaryTotal)
# admin.site.register(News)