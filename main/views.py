from django.shortcuts import render
from .models import News,Sectors,SummaryTotal,LastUpdated,Hero
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import SectorsSerializer,NewsSerializer,LastUpdatedSerializer,SummaryTotalSerializer,HeroSerializer

from django.utils.translation import activate

class MainPageView(APIView):
    def dispatch(self, request, *args, **kwargs):
        if 'HTTP_ACCEPT_LANGUAGE' in request.META:
            lang = request.META['HTTP_ACCEPT_LANGUAGE']
            activate(lang)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        data = {}
        # Hero
        hero_queryset = Hero.objects.all()
        hero_serializer = HeroSerializer(hero_queryset, many=True)
        data['hero'] = hero_serializer.data

        # Last Updated
        last_updated_queryset = LastUpdated.objects.first()
        last_updated_serializer = LastUpdatedSerializer(last_updated_queryset)
        data['last_updated'] = last_updated_serializer.data

        # News
        news_queryset = News.objects.all()
        news_serializer = NewsSerializer(news_queryset, many=True)
        data['news'] = news_serializer.data

        # Sectors
        sectors_queryset = Sectors.objects.all()
        sectors_serializer = SectorsSerializer(sectors_queryset, many=True)
        data['Sectors'] = sectors_serializer.data

        # Total Summary
        summary_queryset = SummaryTotal.objects.all()
        summary_serializer = SummaryTotalSerializer(summary_queryset, many=True)
        data['Total_Summary'] = summary_serializer.data

        return Response(data)

# class MainPageView(APIView):
#     def get(self, request):
#         data = {}
#         # Hero
#         hero_queryset = Hero.objects.all()
#         hero_serializer = HeroSerializer(hero_queryset, many=True)
#         data['hero'] = hero_serializer.data

#         # Last Updated
#         last_updated_queryset = LastUpdated.objects.first()
#         last_updated_serializer = LastUpdatedSerializer(last_updated_queryset)
#         data['last_updated'] = last_updated_serializer.data
#         # News
#         news_queryset = News.objects.all()
#         news_serializer = NewsSerializer(news_queryset, many=True)
#         data['news'] = news_serializer.data

#         # Sectors
#         Sectors_queryset = Sectors.objects.all()
#         sectors_serializer = SectorsSerializer(Sectors_queryset, many=True)
#         data['Sectors'] = sectors_serializer.data

#         # total Summary
#         summary_queryset = SummaryTotal.objects.all()
#         summary_serializer = SummaryTotalSerializer(summary_queryset, many=True)
#         data['Total_Summary'] = summary_serializer.data

        


        

#         return Response(data)   