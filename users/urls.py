from os import name
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'users'
router = DefaultRouter()
router.register( 'freelancer', views.FreelancerAccountViewset )
router.register( 'client', views.ClientAccountViewset)
router.register('freelancer_portfolio', views.PortfolioViewset)


urlpatterns = [
    path('signup', views.UserSignUpView.as_view(), name = 'signup' ),
    path('signin', views.SignInView.as_view(), name = 'signin' ),
    path('signout', views.SignOutView.as_view(), name = 'signout' ),
    path('client/dashboard', views.ClientDashboardView.as_view(), name = 'client dashboard' ),
    path('freelancer/dashboard', views.FreelancerDashboardView.as_view(), name = 'freelancer dashboard' ),
    path('change_password', views.ChangePasswordView.as_view() , name = 'change_password' ),
]

urlpatterns += router.urls
