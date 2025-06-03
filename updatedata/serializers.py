from rest_framework import serializers
from .models import UploadedFile




class ExcelFileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ('file',)


    def validate_file(self, value):
        """
        Check if the uploaded file has the correct extension.
        """
        if not value.name.endswith('.xlsx'):
            raise serializers.ValidationError(
                {"file": "Only .xlsx files are allowed."},
                code='invalid_extension'
            )
        return value    




