from django.conf import settings
from django.db import models
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.utils import timezone

from .managers import CustomUserManager, FreelancerManager
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django_rest_passwordreset.signals import reset_password_token_created
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
    )
from .choices import Gender

from rest_framework_simplejwt.tokens import RefreshToken
# from .tokens import account_activation_token
# Custom Imports
from .choices import Gender
from drf_extra_fields.fields import Base64ImageField



import datetime


AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'custom': 'custom'}
class User(AbstractBaseUser, PermissionsMixin):
    
    # full_name       = models.CharField(max_length=70)
    email = models.EmailField(
        _("Email"),unique=True
        )
    is_freelancer   = models.BooleanField(default=False)
    is_verified     = models.BooleanField(default=True)
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    # auth_provider   = models.CharField(
    #     max_length=255, blank=False,null=False, default=AUTH_PROVIDERS.get('custom')
    #     )
    
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """ 
    as well as create employer of jobseeker instance
    """
    if created:
        Token.objects.create(user=instance)
        
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_secondary_account_instance(sender, instance=None, created=False, **kwargs):
    """ 
    as well as create employer of jobseeker instance
    """
    if created:
        if not instance.is_staff:
            if instance.is_freelancer:
                # if the basic_user is employer create employer instance with full name, primary_contact or email
                freelancer_acc = FreelancerAccount(
                    basic_user = instance,
                    )
                freelancer_acc.save()
        
            else:
                # if the basic_user is jobseeker create JobSeeker instance with full name, mobile or email
                client_acc = ClientAccount(
                    basic_user = instance,
                    )
                client_acc.save()
        

class VerificationCode(models.Model):
    basic_user          = models.OneToOneField('users.User', on_delete=models.CASCADE)
    code                = models.PositiveIntegerField()
    issue_datetime      = models.DateTimeField(auto_now_add=True)
    expiry_datetime     = models.DateTimeField(blank=True, null=True)
    
    
def client_image_upload(instance, filename):
    return '/'.join(['Client', slugify(instance.full_name), filename ])

class ClientAccount(models.Model):
    # on production make on_delete restrict
    basic_user              = models.OneToOneField('users.User', limit_choices_to={'is_freelancer': False}, on_delete=models.CASCADE)    
    full_name               = models.CharField(max_length=50)
    profile_picture         = models.ImageField(upload_to=client_image_upload, height_field=None, width_field=None, blank=True, null=True)  

    age                     = models.PositiveIntegerField(blank = True, default=0)
    gender                  = models.CharField(choices=Gender, max_length=50, blank=True, default=Gender[0][0])
    address                 = models.ForeignKey('job.Address', on_delete=models.RESTRICT, null=True, blank=True)
    contact                 = models.IntegerField(blank=True, null=True )
    profession              = models.CharField(max_length=500, blank=True)
    company_category        = models.CharField(max_length=500, blank=True)
    registered_on           = models.DateTimeField(
                            auto_now_add=True)


    def __str__(self):
        return self.full_name

    @property
    def has_complete_profle(self):
        if self.basic_user and self.age and self.gender and self.contact:
            return True
        return False
        
def freelancer_image_upload(instance, filename):
    return '/'.join(['Freelancer', slugify(instance.full_name), filename ])

class FreelancerAccount(models.Model):
    """
    """
    objects = FreelancerManager()
    
    basic_user              = models.OneToOneField('users.User', limit_choices_to={'is_freelancer': True} , on_delete= models.CASCADE)
    full_name               = models.CharField(max_length=50)
    age                     = models.PositiveIntegerField(blank = True, default=0)
    gender                  = models.CharField(choices=Gender, max_length=50, blank=True,  default=Gender[0][0])
    profile_picture         = models.ImageField(upload_to=freelancer_image_upload, height_field=None, width_field=None, blank=True, null=True)  
    category                = models.ForeignKey('job.Category', on_delete=models.SET_NULL, blank=True, null=True)
    contact                 = models.CharField(max_length=10, blank=True)
    address                 = models.ForeignKey('job.Address', on_delete=models.SET_NULL, blank=True, null=True)
    website                 = models.CharField(max_length=300, blank=True, null=True)  
    skills                  = models.ManyToManyField('job.Skills')
    bio                     = models.CharField(max_length=50)
    description             = models.TextField(blank=True, null=True)
    profile_views           = models.PositiveIntegerField(blank = True, default=0)
    registered_on           = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.full_name
    

    @property
    def has_complete_profle(self):
        if self.basic_user and self.age and self.gender and self.contact:
            return True
        return False