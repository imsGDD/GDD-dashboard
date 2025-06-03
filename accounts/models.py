from django.db import models
from organizations.models import Organization
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _
# Create your models here.




class User(AbstractUser):
    username = models.CharField(max_length = 50, blank = True, null = True, unique = True,verbose_name=_('Username'))
    email = models.EmailField(unique = True, verbose_name=_('Email'))
    organizations = models.ForeignKey(Organization, related_name='user_organization', null=True, blank=True, on_delete=models.CASCADE, verbose_name=_('Organization'))
    otp = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('OTP'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.email    
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('User'))
    profile_picture = models.ImageField(upload_to='users/profile_pictures', default='users/defaultlogo.png', blank=True, verbose_name=_('Profile Picture'))
    first_name = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Last Name'))
    phone_number = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Phone Number'))

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')  



@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        try:
            profile = Profile.objects.get(user=instance)
            profile.save()
        except:
            Profile.objects.create(user=instance)   


