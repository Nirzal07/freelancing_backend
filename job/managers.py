from django.db import models
from random import choice

from rest_framework import views
 
shuffling_list = [
    'title', 'category__title', 'price', 'views',
    '-title', '-category__title', '-price', '-views'
              ]
shuffle_by = choice(shuffling_list)
class JobModelManager(models.Manager):
    def standard(self):
        return super().get_queryset().order_by(shuffle_by)
    
    def featured(self):
        return super().get_queryset().order_by(shuffle_by)
    
    def premium(self):
        return super().get_queryset().order_by(shuffle_by)

    def popular(self):
        # return super().get_queryset().filter(#popular jobs)
        return super().get_queryset().order_by('views')
    
    def recent(self):
        # return super().get_queryset().filter(#popular jobs)
        return super().get_queryset().order_by('announced_on')
    
class CategoryManager(models.Manager):
    def popular(self):
        # return super().get_queryset().filter(#featured jobs)
        return super().get_queryset().order_by('no_of_openings')
    
