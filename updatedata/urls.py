from django.urls import path
from .views import ExcelFileUploadAPIView,ExecuteCommandAPIView

urlpatterns = [
    path('excel-upload/', ExcelFileUploadAPIView.as_view(), name='excel-upload'),
    path('execute-command/', ExecuteCommandAPIView.as_view(), name='execute-command'),

]
