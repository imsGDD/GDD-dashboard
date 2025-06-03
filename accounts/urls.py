from .views import RegisterView,LoginView,LogoutView,PasswordChangeView, PasswordRestEmailVerify
from django.urls import path 


urlpatterns = [
    path('register/', RegisterView.as_view()), 
    path('login/',LoginView.as_view(),),
    path('logout/',LogoutView.as_view(),),

    path('password-reset/<email>/', PasswordRestEmailVerify.as_view()),
    path('password-change/', PasswordChangeView.as_view())
    
]

