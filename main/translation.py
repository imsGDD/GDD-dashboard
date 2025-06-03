from modeltranslation.translator import translator, TranslationOptions
from .models import Hero,News,Sectors,SubSectors

# for Sectors model
class SectorsTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Sectors, SectorsTranslationOptions)


# for Sectors model
class SubSectorsTranslationOptions(TranslationOptions):
    fields = ('name','text','design_shape',)

translator.register(SubSectors, SubSectorsTranslationOptions)


# for Hero model
class HeroTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Hero, HeroTranslationOptions)



# for Hero model
class NewsTranslationOptions(TranslationOptions):
    fields = ('news',)

translator.register(News, NewsTranslationOptions)