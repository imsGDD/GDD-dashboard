from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ExcelFileUploadSerializer
from rest_framework import generics
from .models import UploadedFile
from django.core.management import call_command
from rest_framework.permissions import IsAuthenticated


# Create your views here.



class ExcelFileUploadAPIView(generics.GenericAPIView):
    queryset= UploadedFile.objects.all()
    serializer_class=ExcelFileUploadSerializer
    permission_classes=(IsAuthenticated,)

    
        
    def post(self, request):
        try:
            uploaded_file = UploadedFile.objects.get(id=4)
            serializer = ExcelFileUploadSerializer(uploaded_file, data=request.data)
        except UploadedFile.DoesNotExist:
            serializer = ExcelFileUploadSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'message': 'File uploaded successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'error', 'message': 'Validation failed.', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
 


        


class ExecuteCommandAPIView(APIView):
    permission_classes=(IsAuthenticated,)

    def post(self, request):
        #payload=request.data 
        #sheet_name=payload['sheet_name']
        #uploaded_file_id = payload['uploaded_file_id']
        # if not sheet_name:
        #     return Response({'error': 'Sheet name is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # if not uploaded_file_id:
        #     return Response({'error': 'Uploaded file ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            uploaded_file = UploadedFile.objects.get(id=4)           
            #if sheet_name == "الصفحة الرئيسة":
            call_command('excel_main', uploaded_file.file.path,"الصفحة الرئيسة")
            # sheet_name == "التدخلات":
            call_command('excel_Action_update', uploaded_file.file.path, "التدخلات")
            #elif sheet_name == "الملخص":
            call_command('excel_summary_update', uploaded_file.file.path, "الملخص")
            #elif sheet_name == "حصر الأضرار":
            call_command('excel_report_update', uploaded_file.file.path,"حصر الأضرار" )
                
            call_command('update_translations_report')
            call_command('translate_allactions')
            call_command('translate_news')
    
            return Response({'status': 'success', 'message': 'Data updated successfully.'}, status=status.HTTP_200_OK)
                   
        except UploadedFile.DoesNotExist:
            return Response({'error': 'Uploaded file not found'}, status=status.HTTP_404_NOT_FOUND)
        
       


# (venv) PS D:\New folder (4)> python manage.py excel_main "sheet14-3.xlsx" "الصفحة الرئيسة"   

#(venv) PS D:\Flaw-Track\my-repo\GDD-dashboard> python manage.py translate_allactions

# (venv) PS D:\New folder (4)> python manage.py excel_Action_update "sheet14-3.xlsx" "التدخلات"                           


# (venv) PS D:\New folder (4)> python manage.py excel_summary_update "sheet14-3.xlsx" "الملخص"                            


# (venv) PS D:\New folder (4)> python manage.py excel_report_update "sheet14-3.xlsx" "حصر الأضرار"                        
        

