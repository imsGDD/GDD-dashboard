from django.urls import path, include

from .views import MainPageView


urlpatterns = [

    #########----main page----#######
    path('',MainPageView.as_view())
    
]