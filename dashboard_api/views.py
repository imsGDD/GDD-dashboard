from unittest import case
from .models import Action, Costs, Summary, DamageReport
from .serializers import ActionSerializer, CostSerializer, SummarySerializer, DamageReportSerializer
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .mypagination import ActionAllPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import activate



class ActionAllListView(generics.ListAPIView):
    serializer_class = ActionSerializer
    queryset = Action.objects.all()
    pagination_class = ActionAllPagination


class ActionPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ActionListView(generics.ListAPIView):
    serializer_class = ActionSerializer
    pagination_class = ActionPagination



    def get_queryset(self):
        sector_id = self.kwargs.get('id')
        return Action.objects.filter(sector_id=sector_id).order_by('id')
    # def get_queryset(self):
    #     sector_name = self.kwargs.get('sector_name')  
    #     if sector_name:
    #         return Action.objects.filter(sector__name=sector_name)
    #     else:
    #         return Action.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())  

        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True, context={'request': request})

        return self.get_paginated_response(serializer.data)

########################################################################
    #-----------------------------Costs------------------------------

class CostListView(generics.ListAPIView):
    serializer_class = CostSerializer
    queryset = Costs.objects.all()

#
class SummaryListView(generics.ListAPIView):
    serializer_class = SummarySerializer
    def dispatch(self, request, *args, **kwargs):
        if 'HTTP_ACCEPT_LANGUAGE' in request.META:
            lang = request.META['HTTP_ACCEPT_LANGUAGE']
            activate(lang)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        sector_id = self.kwargs.get('sector_id')  
        if sector_id:
            return Summary.objects.filter(sector__id=sector_id)
        else:
            return Summary.objects.all()
        
    # def get_queryset(self):
    #     sector_name = self.kwargs.get('sector_name')  
    #     sector_id = self.kwargs.get('sector_id')
    #     if sector_name:
    #         return Summary.objects.filter(sector__name=sector_name)
    #     else:
    #         return Summary.objects.all()    

#################################-----damage report------###########################################
from django.utils import translation        

class DamageReportListView(generics.ListAPIView):
    #queryset = DamageReport.objects.all()
    serializer_class = DamageReportSerializer
    pagination_class = ActionAllPagination

    def get_queryset(self):
        
        sector = self.kwargs.get('sector')  
        if sector:
            return DamageReport.objects.filter(sector=sector)
        else:
            return DamageReport.objects.all()
        
