from django.urls import path, include

from .views import ActionListView, ActionAllListView, CostListView,SummaryListView,DamageReportListView


urlpatterns = [
    path('action-all/', ActionAllListView.as_view()), # to get all action
    path('actions/sector/<int:id>/', ActionListView.as_view()), #to get  actions by sector id
    #path('actions/sector/<str:sector_name>/', ActionListView.as_view()), #to get  actions by sector name

    ##################cost#####################
    #path('cost-action/<int:id>/', CostListView.as_view()),
    path('summary/', SummaryListView.as_view()),   # to get all summary
    path('summary/<int:sector_id>/', SummaryListView.as_view(), name='summary-list-by-sector'),  #to get  summary by sector id
    #path('summary/<int:sector_id>/<str:sector_name>/', SummaryListView.as_view(), name='summary-list-by-sector-name'),  #to get  summary by sector name

    path('damage-reports/<str:sector>/', DamageReportListView.as_view(), name='damage-report-list'),
    path('damage-reports/', DamageReportListView.as_view(), name='damage-report-list'),

    
    
]

