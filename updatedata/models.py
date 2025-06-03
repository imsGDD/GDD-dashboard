from django.db import models
from django.utils.translation import gettext as _

# Create your models here.


class UploadedFile(models.Model):
    file = models.FileField(upload_to='excel_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = _('File Update')
        verbose_name_plural = _('File Update')


    # def __str__(self):
    #     return self.file