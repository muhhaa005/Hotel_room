from .models import *
from modeltranslation.translator import TranslationOptions, register

@register(City)
class ProductTranslationOptions(TranslationOptions):
    fields = ('city_name',)


@register(Hotel)
class ProductTranslationOptions(TranslationOptions):
    fields = ('hotel_name', 'description')


@register(Rooms)
class ProductTranslationOptions(TranslationOptions):
    fields = ('description',)
