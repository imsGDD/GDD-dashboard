from django.contrib import admin
from .models import Action, Sector, Tag, ChildAction, Costs, Summary, DamageReport,Card,Chart,ChartData




# class CardInline(admin.TabularInline):
#     model = Card   
#     extra=0        

# class DamageReportAdmin(admin.ModelAdmin):
#     list_display=['sector','sub_sector','sub_classification','damage_sector','damage','damage_value_number','damage_value_percentage']
#     inlines = [CardInline]

from modeltranslation.admin import TranslationAdmin

class ActionAdmin(TranslationAdmin):
    search_fields=['damage_ar']
    list_display=['id','damage_ar','action_type_ar','action_value']

class SectorAdmin(TranslationAdmin):
    pass
class TagAdmin(TranslationAdmin):
    pass
class ChildActionAdmin(TranslationAdmin):
    search_fields=['action_type_ar']
class CostsAdmin(TranslationAdmin):
    pass

# class SummaryAdmin(TranslationAdmin):
#     pass
class DamageReportAdmin(TranslationAdmin):
    list_display=['sector','key','sub_sector_ar','sub_classification_ar','damage_sector_ar','damage_ar','damage_value_number','damage_value_percentage','updated_at']

    
class CardAdmin(TranslationAdmin):
    pass
class ChartAdmin(TranslationAdmin):
    pass
class ChartDataAdmin(TranslationAdmin):
    list_display=['name_ar','number','percentage','updated_at']
    #pass
    search_fields =['name_ar']



admin.site.register(Action,ActionAdmin)
admin.site.register(Sector,SectorAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(ChildAction,ChildActionAdmin)
admin.site.register(Costs,CostsAdmin)
admin.site.register(Summary)
admin.site.register(DamageReport,DamageReportAdmin)
admin.site.register(Card,CardAdmin)
admin.site.register(Chart,ChartAdmin)
admin.site.register(ChartData,ChartDataAdmin)






# admin.site.register(Action)
# admin.site.register(Sector)
# admin.site.register(Tag)
# admin.site.register(ChildAction)
# admin.site.register(Costs)
# admin.site.register(Summary)
# admin.site.register(DamageReport,DamageReportAdmin)
# admin.site.register(Card)
# admin.site.register(Chart)
# admin.site.register(ChartData)


