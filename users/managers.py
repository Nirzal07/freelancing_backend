from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.db import models

class CustomUserManager(BaseUserManager):
    """custom user model with email as the unique identifier"""

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Email cannot be blank'))
        # validates if the entered e_o_p is either an email or phone
        else:
            user = self.model(
                email=email, **extra_fields)
            
            user.set_password(password)
            user.save()
            return user

    def create_superuser(self, email, password, **extra_fields):
        """creates a superuser with email and password"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
    
class FreelancerManager(models.Manager):
    def featured(self):
        # return super().get_queryset().filter(#featured jobs)
        return super().get_queryset().order_by('')