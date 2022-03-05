#django
from django.contrib.auth import login, logout, authenticate
from django.core.mail import message
from django.urls import reverse
import datetime
from django.utils import timezone

# from rest framework
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, UpdateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet


#custom
# from .tokens import account_activation_token
# from .tokens import AccountActivationTokenGenerator
# from .verification import verification_code_or_token
from .serializers import (
    GoogleAuthSignUpSerializer,
    UserAccountSerializer,
#   SigninSerializer,
    ClientAccountSerializer,
    FreelancerAccountSerializer,
    ChangePasswordSerializer,
    GoogleAuthSignInSerializer,
    GoogleAuthSignUpSerializer,
    FacebookAuthSignInSerializer,
    FacebookAuthSignUpSerializer
    )
import job.models as job_models
from .models import User, ClientAccount, FreelancerAccount, VerificationCode



class UserSignUpView(CreateAPIView):
    serializer_class = UserAccountSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserAccountSerializer(data= request.data)
        if User.objects.filter(
            email = self.request.data['email']).exists():
            return Response({'error': 'An account with this email address already exists'}, status= status.HTTP_202_ACCEPTED)
        if serializer.is_valid():
            user = serializer.create(serializer.validated_data)
            # after adding verification remove the two lines below
            user.is_verified = True
            user.save()
            token = Token.objects.get(user= user)

            # update full name of employer/jobseeker account of the created user
            # full_name = serializer.validated_data['full_name']
            if user.is_freelancer:
                user_secondary = FreelancerAccount.objects.get(basic_user = user)
            else:
                user_secondary = ClientAccount.objects.get(basic_user = user) 
                
            # user_secondary.full_name = full_name
            # user_secondary.save()
            data = {
                # 'message': f'A verification code is sent to {user.email_or_phone}', 
                'message': 'User Signed Up Successfully',
                # "user_id": user.id,
                # "secondary_user_id": user_secondary.id,
                # "is_freelancer": user.is_freelancer,
                # # the below line might not be necessary
                # "has_complete_profile": user_secondary.has_complete_profile,
                # "email":user.email,
                # 'full_name' : user_secondary.full_name,
                # "token": token.key
                }
            return Response(data, status= status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status= status.HTTP_200_OK)
     

class SignInView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = self.request.data["email"]
        password = self.request.data["password"]
        user = authenticate(email=email, password= password)
        if user and user.is_verified:
            if user.is_freelancer:
                user_secondary = FreelancerAccount.objects.get(basic_user = user)
            else:
                user_secondary = ClientAccount.objects.get(basic_user = user) 
            if Token.objects.filter(user= user).exists():
                Token.objects.filter(user= user).delete()
            token= Token.objects.create(user= user)
            data = {
                "message": "User logged in successful", 
                "user_id": user.id,
                "secondary_user_id": user_secondary.id,
                "is_employer": user.is_freelancer,
                # the below line might not be necessary
                "has_complete_profile": user_secondary.has_complete_profile,
                "email":user.email, 
                'full_name' : user_secondary.full_name,
                "token": token.key
                }
            
            return Response(data, status= status.HTTP_200_OK)
        elif user and not user.is_verified:
            return Response({"message": "User not verified"}, status= status.HTTP_200_OK)
        return Response({"message": "Invalid Login Credentials"}, status= status.HTTP_200_OK)
    
        
class BasicUserView(APIView):
    """
    update this view to change user's account type if has_complete_profile is false
    """
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        user = self.request.user
        serializer = UserAccountSerializer(user)
        serializer.data.pop('is_employer')
        return Response(
            {'email_or_phone': serializer.data["email_or_phone"],
             'full_name': serializer.data["full_name"]}, 
            status= status.HTTP_200_OK)     

        
    def patch(self, request):
        user = self.request.user
        serializer = UserAccountSerializer(data = request.data, partial=True)
        if serializer.is_valid():
            full_name = serializer.validated_data['full_name']
            user.full_name = full_name
            user.save()
            return Response({'message':"User's Full Name updated successfully"}, status= status.HTTP_200_OK)     
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class SignOutView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request, *args, **kwargs):
        Token.objects.filter(user= request.user).delete()
        return Response({'message': "User Logged Out Successfully"})

class ClientAccountViewset(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = ClientAccount.objects.all()
    serializer_class = ClientAccountSerializer
    # permission_classes = (IsCreater,)
    
class FreelancerAccountViewset(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = FreelancerAccount.objects.all()
    serializer_class = FreelancerAccountSerializer

class FreelancerDashboardView(APIView):
    """
    To get the list of a applied of a particular job

    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """To get the list of a users Favourites job"""
        if self.request.user.is_freelancer:
            
            freelancer = FreelancerAccount.objects.get(basic_user = self.request.user)
            try:
                proposed_jobs = job_models.ProposedJobs.objects.get(freelancer= freelancer)
                proposed_jobs_count = proposed_jobs.jobs.all().count()
            except job_models.ProposedJobs.DoesNotExist:
                proposed_jobs_count = 0
            
            try:
                favourites = job_models.Favourites.objects.get(user= self.request.user)
                favourites_count = favourites.favourite_jobs.all().count()
            except job_models.Favourites.DoesNotExist:
                favourites_count = 0
            has_complete_profile = freelancer.has_complete_profile
            
            return Response({
                'proposed_jobs_count': proposed_jobs_count, 
                'favourites_count' : favourites_count,
                'has_complete_profile': has_complete_profile
                }, status=status.HTTP_200_OK)
            
        return Response({'message': "Employer"}, status=status.HTTP_200_OK)
                  
class ClientDashboardView(APIView):
    """
    To get the list of a applied of a particular job

    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """To get the list of a users Favourites job"""
        if not self.request.user.is_freelancer:
            
            client = ClientAccount.objects.get(basic_user = self.request.user)
            try:
                posted_jobs = job_models.Vacancy.jobs.filter(client= client)
                posted_jobs_count = posted_jobs.count()
            except job_models.Vacancy.DoesNotExist:
                posted_jobs_count = 0
            
            try:
                proposants = job_models.Proposals.objects.filter(client= client)
                proposants_count = 0
                for appli in proposants:
                    proposants_count += appli.proposants.count()
            except job_models.Proposals.DoesNotExist:
                proposants_count = 0
                
            has_complete_profile = client.has_complete_profile
            
            return Response({
                'posted_jobs_count': posted_jobs_count,
                'proposants_count' : proposants_count,
                'has_complete_profile': has_complete_profile
                }, status=status.HTTP_200_OK)
            
        return Response({'message': "Freelancer"}, status=status.HTTP_200_OK)
         
class ChangePasswordView(UpdateAPIView):
    model = User
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # check whether the old password is correct or not
            if not self.object.check_password(serializer.validated_data['old_password']):
                return Response({'message': 'The password you\'ve entered is incorrect'},  status=status.HTTP_200_OK)
            
            self.object.set_password(serializer.validated_data['new_password'])
            self.object.save()
            return Response({'message': 'Password updated Successfully!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccountVerificationView(APIView):

    """
    Verify registered user with token or verification code
    """
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        if not self.request.user.is_verified:
            verification_code_or_token(user=self.request.user)
            return Response({"message":"Verification Code is sent to the user"}, status=status.HTTP_200_OK)
        return Response({"message":"This account was already verified"}, status=status.HTTP_200_OK) 
    
    def post(self, request):
        if not self.request.user.is_verified:
            # verification with token for email only
            if 'token' in request.data:
                if account_activation_token.check_token(self.request.user, request.data['token']):
                    user = self.request.user
                    user.is_verified= True
                    user.save()
                    return Response({"message":"Account activation successfull"}, status=status.HTTP_200_OK)
                else:
                    return Response({"error":"Invalid or Expired token"}, status=status.HTTP_200_OK)
            
            # verfication with verification code for email and phone
            if 'code' in request.data:
                provided_verification_code = request.data['code']
                try:
                    verification_code = VerificationCode.objects.get(user = self.request.user)
                    
                    if timezone.now() > verification_code.expiry_datetime:
                        verification_code.delete()
                        return Response({"error":"Verification code is expired"}, status=status.HTTP_200_OK)
                    
                    elif verification_code.code != provided_verification_code:
                        return Response({"error":"Verification code is invalid"}, status=status.HTTP_200_OK)
                        
                    elif verification_code.code == provided_verification_code:
                        verification_code.delete()
                        return Response({'message':'Account Activation Successful!'}, status=status.HTTP_200_OK)
                    
                    
                except VerificationCode.DoesNotExist:
                    return Response({"error":"Verification code is invalid or expired"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                Response({'error': 'Invalid Parameters were provided'})
        else:
            return Response({"message":"This account was already verified"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        # social auth
class GoogleAuthSignUpView(GenericAPIView):

    serializer_class = GoogleAuthSignUpSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data))
        return Response(data, status=status.HTTP_200_OK)

class GoogleAuthSignInView(GenericAPIView):

    serializer_class = GoogleAuthSignInSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data))
        return Response(data, status=status.HTTP_200_OK)

class FacebookAuthSignUpView(GenericAPIView):

    serializer_class = FacebookAuthSignUpSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an access token as from facebook to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data))
        return Response(data, status=status.HTTP_200_OK)

class FacebookAuthSignInView(GenericAPIView):

    serializer_class = FacebookAuthSignInSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an access token as from facebook to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data))
        return Response(data, status=status.HTTP_200_OK)
