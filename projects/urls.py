from django.urls import path, include

from .views import helperView,ProjectView


urlpatterns = [

    path('help/',helperView.as_view()),
    path('project/',ProjectView.as_view()),
    path('project/<int:project_id>/',ProjectView.as_view()),
    
]