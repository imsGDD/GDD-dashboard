from modeltranslation.translator import translator, TranslationOptions
from .models import Sector,Tag,Action,ChildAction,Costs,Summary,DamageReport,Card,Chart,ChartData

# for Sectors model
class SectorTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Sector, SectorTranslationOptions)


# for Tag model
class TagTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Tag, TagTranslationOptions)


# for Action model
class ActionTranslationOptions(TranslationOptions):
    fields = ('damage','sub_sector','subclassification','action_type',)

translator.register(Action, ActionTranslationOptions)


# for ChildAction model
class ChildActionTranslationOptions(TranslationOptions):
    fields = ('action_type',)

translator.register(ChildAction, ChildActionTranslationOptions)



# for Costs model
class CostsTranslationOptions(TranslationOptions):
    fields = ('damage_summary','sub_sector','scope_of_intervention',)

translator.register(Costs, CostsTranslationOptions)


# for Summary model
# class SummaryTranslationOptions(TranslationOptions):
#     fields = ('sector','cost',)

# translator.register(Summary, SummaryTranslationOptions)


# for DamageReport model
class DamageReportTranslationOptions(TranslationOptions):
    fields = ('sector','sub_sector','sub_classification','damage_sector','damage','damage_value_type',)

translator.register(DamageReport, DamageReportTranslationOptions)



# for Card model
class CardTranslationOptions(TranslationOptions):
    fields = ('title',)

translator.register(Card, CardTranslationOptions)


# for Chart model
class ChartTranslationOptions(TranslationOptions):
    fields = ('type','icon_code',)

translator.register(Chart, ChartTranslationOptions)


# for ChartData model
class ChartDataTranslationOptions(TranslationOptions):
    fields = ('name','data_type',)

translator.register(ChartData, ChartDataTranslationOptions)



