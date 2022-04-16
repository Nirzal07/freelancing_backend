from django.core.exceptions import PermissionDenied
from django.http import request
from decouple import config
# import facebook
# from .facebook import Facebook
from rest_framework import serializers
from .models import User, ClientAccount, FreelancerAccount

from job.models import Category,  Address, Skills
from rest_framework.fields import CurrentUserDefault
# from . import google
# from .social_auth import social_user_signup, social_user_signin
import os
from rest_framework.exceptions import AuthenticationFailed
from drf_extra_fields.fields import Base64ImageField


class UserAccountSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ('id', 'is_freelancer', 'email', 'password', "full_name")
        write_only_fields = ('password',)
        read_only_fields = ('id',)
        extra_kwargs = {'is_freelancer': {'required': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            is_freelancer = validated_data['is_freelancer'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class SigninSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField()
    password = serializers.CharField()

class ReadUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'is_freelancer', 'email')

class ClientAccountSerializer(serializers.ModelSerializer):
    profile_picture=Base64ImageField(required= False)
    basic_user = serializers.StringRelatedField(
        read_only=True, 
        default=serializers.CurrentUserDefault()
        )
    
    address = serializers.SlugRelatedField(
        read_only=False, 
        slug_field='title',
        allow_null = True, 
        queryset= Address.objects.all()
        )
    has_complete_profile = serializers.ReadOnlyField()

    class Meta:
        model = ClientAccount
        fields = '__all__'
        read_only_fields = ["registered_date"]
        extra_kwargs = {'url': {'lookup_field': 'slug'}}



class FreelancerAccountSerializer(serializers.ModelSerializer):
    basic_user = serializers.StringRelatedField(
        read_only=True, 
        default=serializers.CurrentUserDefault()
        )
    
    address = serializers.SlugRelatedField(
        read_only=False, 
        slug_field='title',
        allow_null = True,
        queryset= Address.objects.all()
        )
    
    skills = serializers.SlugRelatedField(
        many=True,
        read_only=False, 
        slug_field='title',
        allow_null = True,
        queryset= Skills.objects.all()
        )

    category = serializers.SlugRelatedField(
        read_only=False, 
        slug_field='title',
        allow_null = True,
        queryset= Category.objects.all()
        )

    profile_picture=Base64ImageField(required= True)
    
    has_complete_profile = serializers.ReadOnlyField()

    class Meta:
        model = FreelancerAccount
        fields = '__all__'
        read_only_fields = [ "registered_date", "slug"]
        extra_kwargs = {'price': {'write_only': True}, 'url': {'lookup_field': 'slug'}}




class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required = True)
    new_password = serializers.CharField(required = True)
    
    
    
class FacebookAuthSignUpSerializer(serializers.Serializer):
    """Handles serialization of facebook related data"""
    auth_token = serializers.CharField()
    full_name = serializers.CharField(required=True)
    is_employer = serializers.BooleanField()

    def validate(self, attrs):
        user_data = Facebook.validate(attrs['auth_token'])
        is_employer= attrs['is_employer']
        try:
            user_id = user_data['id']
            email = user_data['email']
            name = user_data['name']
            provider = 'facebook'
            return social_user_signup(
                provider=provider,
                user_id=user_id,
                email=email,
                name=name,
                is_employer= is_employer
            )
        except Exception as identifier:

            raise serializers.ValidationError(
                'The token  is invalid or expired. Please signin again.'
            )

class FacebookAuthSignInSerializer(serializers.Serializer):
    """Handles serialization of facebook related data"""
    auth_token = serializers.CharField()
    # is_employer = serializers.BooleanField()

    def validate(self, attrs):
        user_data = Facebook.validate(attrs['auth_token'])
        # is_employer= attrs['is_employer']
        try:
            user_id = user_data['id']
            email = user_data['email']
            name = user_data['name']
            provider = 'facebook'
            return social_user_signin(
                provider=provider,
                user_id=user_id,
                email=email,
                name=name,
                # is_employer= is_employer
            )
        except Exception as identifier:

            raise serializers.ValidationError(
                'The token  is invalid or expired. Please signin again.'
            )

class GoogleAuthSignUpSerializer(serializers.Serializer):
    auth_token = serializers.CharField()
    is_employer = serializers.BooleanField()
    
    def validate(self, attrs):
        user_data = google.Google.validate(attrs['auth_token'])
        is_employer = attrs['is_employer']
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please signin again.'
            )

        if user_data['aud'] != config('GOOGLE_CLIENT_ID'): 
            # replace this value with ClientId from env Var
            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return social_user_signup(
            provider=provider, 
            user_id=user_id, 
            email=email, 
            name=name,
            is_employer= is_employer
            )

class GoogleAuthSignInSerializer(serializers.Serializer):
    auth_token = serializers.CharField()
    # is_employer = serializers.BooleanField()
    
    def validate(self, attrs):
        user_data = google.Google.validate(attrs['auth_token'])
        # is_employer = attrs['is_employer']
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please signin again.'
            )

        if user_data['aud'] != config('GOOGLE_CLIENT_ID'):

            raise AuthenticationFailed('Something went wrong')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return social_user_signin(
            provider=provider, 
            user_id=user_id, 
            email=email, 
            name=name,
            # is_employer= is_employer
            )


