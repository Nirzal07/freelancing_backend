from django.db.models import base
from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(
    'jobs',
    views.JobView,
    basename='jobs'
    )
    

app_name = 'job'
urlpatterns= [
    path('', include(router.urls)),
    # path('favourites', views.FavouritesView.as_view(), name= 'favourites'),
    # path('applied', views.AppliedJobsView.as_view(), name= 'applied_jobs'),
    # path('proposants', views.ApplicantsView.as_view(), name= 'proposants'),
    # path('featured', views.FeaturedJobsListView.as_view(), name= 'featured'),
    # path('popular', views.PopularJobsListView.as_view(), name= 'popular'),
    # path('recent', views.RecentJobsListView.as_view(), name= 'recent'),
    # path('posted', views.PostedJobsListView.as_view(), name= 'posted_jobs_list'),
    
    # # Prod Note: remove the line below and its import
    # path('populate', populate.PopulateDB.as_view(), name= 'populate')
]