from os import name
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    GoogleAuthSignUpView,
    GoogleAuthSignInView,
    FacebookAuthSignUpView,
    FacebookAuthSignInView
    # AccountVerificationView,
    )


app_name = 'users'
freelancer_account_router = DefaultRouter()
freelancer_account_router.register(
    'freelancer',
    views.FreelancerAccountViewset,
    basename='freelancer_account'
    )

client_account_router = DefaultRouter()
client_account_router.register(
    'client',
    views.ClientAccountViewset,
    basename='client_account'
    )

urlpatterns = [
    path('', include(freelancer_account_router.urls)),
    path('', include(client_account_router.urls)),
    path('signup', views.UserSignUpView.as_view(), name = 'signup' ),
    # path('verification', views.AccountVerificationView.as_view(), name = 'account_activation' ),
    path('signin', views.SignInView.as_view(), name = 'signin' ),
    path('signout', views.SignOutView.as_view(), name = 'signout' ),
    path('client/dashboard', views.ClientDashboardView.as_view(), name = 'client dashboard' ),
    path('freelancer/dashboard', views.FreelancerDashboardView.as_view(), name = 'freelancer dashboard' ),
    # path('basicuser', views.BasicUserView.as_view(), name = 'basicuser' ),
    # path('signin_google', GoogleAuthSignInView.as_view()),
    # path('signup_google', GoogleAuthSignUpView.as_view()),
    # path('signin_facebook', FacebookAuthSignInView.as_view()),
    # path('signup_facebook', FacebookAuthSignUpView.as_view()),
    path('change_password', views.ChangePasswordView.as_view() , name = 'change_password' ),
]